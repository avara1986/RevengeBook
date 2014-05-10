from revengeapp.models import revengePoint, revengePointCat


def get_revenge_points(request):
    revCats = revengePointCat.objects.all()
    revPoints = revengePoint.objects.all()
    return {'revPoints': revPoints,
            'revCats': revCats}
