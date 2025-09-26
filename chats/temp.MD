all() - достать все элементы
filter(pk=pk, date_created=timezone.now()) - достает только объекты которые попадают под фильтр
first() - достает самый первый элемент из тех что мы запросили (all, filter)
last() - достает самый последний элемент из тех что мы запросили (all, filter)
get(pk=pk, date_created=timezone.now()) - достает только 1 объект который попадает под фильтр
add() - добавляет элементы к ManyToManyField
delete() - удаляет объект (
    user = User.objects.get(pk=1)
    user.delete()
)

Методы оптимизации select(ов):
prefetch_related() = работает для ManyToMany и ManyToOne
select_related() = работает для OneToOne и ForeignKey