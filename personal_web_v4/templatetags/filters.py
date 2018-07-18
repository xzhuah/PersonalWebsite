from django import template

register = template.Library()


@register.filter
def get_percent(arg):
    return str(arg/100)

@register.filter
def get_pos(arg):
    #return "right"
    #print(arg)
    a = int(arg[-1:])
    if a%2==0:
        return "right"
    else:
        return "left"


@register.filter
def get_img(arg):
    return "images/portfolio/"+str(arg)


