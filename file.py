
def f():
    dict = {}
    for x in range(-5,6):
        try:
                f = x**2  
                dict[x]=f
        except ZeroDivisionError:
            pass
        
    return dict
    
