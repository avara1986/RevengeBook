from revengeapp.models import revengeCat


def get_revenge_points(request):
    revCats = revengeCat.objects.all()
    return {'revCats': revCats,}
