from django import template

register = template.Library()

@register.filter(is_safe=True)
def comment_display(text):
	new_text = ""
	for n in text:
		if n != '#':
			new_text = new_text + n
		else:
			new_text = new_text + '</br>'
	return new_text

@register.filter
def modulo(num, val):
	return num % val == 0

@register.filter
def sub(num, val):
	return num-val

@register.filter
def mul(num, val):
	return num*val

@register.filter
def diveuclid(num, val):
	return num//val

@register.filter
def range_django(num):
	return range(num)

@register.filter
def div(num, val):
	return num/val

@register.filter
def mod(num, val):
	return num%val

@register.filter
def arrondi(num, val):
	return int(num*pow(10, val))/pow(10, val)

@register.filter
def percent(num):
	return "{0:.2f}%".format(num*100)
