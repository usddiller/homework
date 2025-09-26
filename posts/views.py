import requests
from datetime import datetime, timedelta

from django.utils import timezone
from django.core.cache import cache
from django.conf import settings

from rest_framework import viewsets, permissions, status, serializers
from rest_framework.decorators import action
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import Article


api_key = getattr(settings, "NEWSAPI_KEY", None)


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = [
            "id",
            "source_id",
            "source_name",
            "author",
            "title",
            "description",
            "url",
            "url_to_image",
            "published_at",
            "content",
        ]


class ArticleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET  /api/v1/articles/?fresh=true&title_contains=...
    POST /api/v1/articles/update/   (тянет из NewsAPI, сохраняет только новые)
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.AllowAny]
    swagger_tags = ["Articles"]

    @swagger_auto_schema(
        operation_description="Список статей. Параметры: fresh=true (за 24ч), title_contains=<строка>.",
        tags=["Articles"],
        manual_parameters=[
            openapi.Parameter(
                name="fresh",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="true/false — только статьи за последние 24 часа",
            ),
            openapi.Parameter(
                name="title_contains",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="поиск по заголовку (icontains)",
            ),
        ],
        responses={200: ArticleSerializer(many=True)},
    )
    def list(self, request, *args, **kwargs):
        fresh = (request.query_params.get("fresh", "").lower() == "true")
        title_contains = request.query_params.get("title_contains", "").strip()

        cache_key = f"articles:list:{fresh}:{title_contains or '_'}"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        qs = self.get_queryset()
        if fresh:
            since = timezone.now() - timedelta(hours=24)
            qs = qs.filter(published_at__gte=since)
        if title_contains:
            qs = qs.filter(title__icontains=title_contains)

        data = self.get_serializer(qs, many=True).data
        cache.set(cache_key, data, 60 * 10)  # 10 минут
        return Response(data)

    @swagger_auto_schema(
        operation_description=(
            "Подтягивает статьи из NewsAPI и сохраняет только новые (по уникальному url). "
            "Кэширует результат на 30 минут. "
            "Опциональные поля в JSON: {\"q\": \"python\", \"country\": \"us\", \"force\": true}"
        ),
        tags=["Articles"],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "q": openapi.Schema(type=openapi.TYPE_STRING),
                "country": openapi.Schema(type=openapi.TYPE_STRING),
                "force": openapi.Schema(type=openapi.TYPE_BOOLEAN),
            },
        ),
        responses={
            200: openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "fetched": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "inserted": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "skipped": openapi.Schema(type=openapi.TYPE_INTEGER),
                    "source": openapi.Schema(type=openapi.TYPE_STRING),
                    "params": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "q": openapi.Schema(type=openapi.TYPE_STRING),
                            "country": openapi.Schema(type=openapi.TYPE_STRING),
                        },
                    ),
                },
            ),
            400: "NEWSAPI_KEY not set",
            502: "newsapi error",
        },
    )
    @action(methods=["post"], detail=False, url_path="update", permission_classes=[permissions.AllowAny])
    def pull(self, request):
        # кэш результата обновления (лимит по API)
        cache_key = "articles:update:last"
        if not request.data.get("force"):
            cached = cache.get(cache_key)
            if cached is not None:
                return Response(cached)

        if not api_key:
            return Response({"detail": "NEWSAPI_KEY not set"}, status=status.HTTP_400_BAD_REQUEST)

        q = (request.data.get("q") or "").strip()
        country = (request.data.get("country") or "us").strip()

        # если есть q -> everything, иначе top-headlines по стране
        if q:
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": q,
                "sortBy": "publishedAt",
                "pageSize": 100,
                "language": "en",
                "apiKey": api_key,
            }
            source_name = "everything"
        else:
            url = "https://newsapi.org/v2/top-headlines"
            params = {"country": country, "pageSize": 100, "apiKey": api_key}
            source_name = "top-headlines"

        try:
            r = requests.get(url, params=params, timeout=10)
            r.raise_for_status()
        except requests.RequestException as e:
            return Response({"detail": f"newsapi error: {e}"}, status=502)

        payload = r.json() or {}
        items = payload.get("articles") or []

        urls = [a.get("url") for a in items if a.get("url")]
        existing = set(
            Article.objects.filter(url__in=urls).values_list("url", flat=True)
        )

        new_objs = []
        for a in items:
            u = a.get("url")
            if not u or u in existing:
                continue
            src = a.get("source") or {}

            published_at = a.get("publishedAt")
            if published_at:
                try:
                    # ISO8601, часто с 'Z'
                    if published_at.endswith("Z"):
                        published_at = datetime.fromisoformat(
                            published_at.replace("Z", "+00:00")
                        )
                    else:
                        published_at = datetime.fromisoformat(published_at)
                except Exception:
                    published_at = timezone.now()
            else:
                published_at = timezone.now()

            new_objs.append(
                Article(
                    source_id=(src.get("id") or None),
                    source_name=(src.get("name") or ""),
                    author=(a.get("author") or ""),
                    title=(a.get("title") or "")[:500],
                    description=(a.get("description") or "") or "",
                    url=u,
                    url_to_image=(a.get("urlToImage") or "") or "",
                    published_at=published_at,
                    content=(a.get("content") or "") or "",
                )
            )

        if new_objs:
            Article.objects.bulk_create(new_objs, ignore_conflicts=True)

        result = {
            "fetched": len(items),
            "inserted": len(new_objs),
            "skipped": len(items) - len(new_objs),
            "source": source_name,
            "params": {"q": q, "country": country},
        }
        cache.set(cache_key, result, 60 * 30)  # 30 минут
        return Response(result)
