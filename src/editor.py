from client.math.curve import curve
class editor():
    def eval_curve(self,**kwargs):
        crv = curve( kwargs['points'] ) 
        return { "value" : crv.value_at(kwargs['t'] ) }
