def HSL_to_RGB(h,s,l):
    ''' Converts HSL colorspace (Hue/Saturation/Value) to RGB colorspace.
        Formula from http://www.easyrgb.com/math.php?MATH=M19#text19
        
        Input:
        h (float) : Hue (0...1, but can be above or below
        (This is a rotation around the chromatic circle))
        s (float) : Saturation (0...1)    (0=toward grey, 1=pure color)
        l (float) : Lightness (0...1)     (0=black 0.5=pure color 1=white)
        
        Ouput:
        (r,g,b) (integers 0...255) : Corresponding RGB values
        
        Examples:
        >>> print HSL_to_RGB(0.7,0.7,0.6)
        (110, 82, 224)
        >>> r,g,b = HSL_to_RGB(0.7,0.7,0.6)
        >>> print g
        82
    '''
    def Hue_2_RGB( v1, v2, vH ):
        while vH<0.0: 
            vH += 1.0
        while vH>1.0:
            vH -= 1.0
        if 6*vH < 1.0 :
            return v1 + (v2-v1)*6.0*vH
        if 2*vH < 1.0 :
            return v2
        if 3*vH < 2.0 :
            return v1 + (v2-v1)*((2.0/3.0)-vH)*6.0
        return v1
    
    if not (0 <= s <=1):
        raise ValueError#, "s (saturation) parameter must be between 0 and 1."
    if not (0 <= l <=1):
        raise ValueError#, "l (lightness) parameter must be between 0 and 1."
    
    r,b,g = (l,)*3
    if s!=0.0:
        if l<0.5 :
            var_2 = l * ( 1.0 + s )
        else     :
            var_2 = ( l + s ) - ( s * l )
        var_1 = 2.0 * l - var_2
        r = Hue_2_RGB( var_1, var_2, h + ( 1.0 / 3.0 ) )
        g = Hue_2_RGB( var_1, var_2, h )
        b = Hue_2_RGB( var_1, var_2, h - ( 1.0 / 3.0 ) )

    return (r,g,b)


def RGB_to_HSL(r,g,b):
    ''' Conver:ts RGB colorspace to HSL (Hue/Saturation/Value) colorspace.
        Formula from http://www.easyrgb.com/math.php?MATH=M18#text18
        
        Input:
        (r,g,b) (integers 0...255) : RGB values
        
        Ouput:
        (h,s,l) (floats 0...1): corresponding HSL values
        
        Example:
        >>> print RGB_to_HSL(110,82,224)
        (0.69953051643192476, 0.69607843137254899, 0.59999999999999998)
        >>> h,s,l = RGB_to_HSL(110,82,224)
        >>> print s
        0.696078431373
        '''
    if not (0 <= r <=1): raise ValueError#,"r (red) parameter must be between 0 and 255."
    if not (0 <= g <=1): raise ValueError#,"g (green) parameter must be between 0 and 255."
    if not (0 <= b <=1): raise ValueError#,"b (blue) parameter must be between 0 and 255."
    
    var_R = r
    var_G = g
    var_B = b
    
    var_Min = min( var_R, var_G, var_B )    # Min. value of RGB
    var_Max = max( var_R, var_G, var_B )    # Max. value of RGB
    del_Max = var_Max - var_Min             # Delta RGB value
    
    l = ( var_Max + var_Min ) / 2.0
    h = 0.0
    s = 0.0
    if del_Max!=0.0:
        if l<0.5: s = del_Max / ( var_Max + var_Min )
        else:     s = del_Max / ( 2.0 - var_Max - var_Min )
        del_R = ( ( ( var_Max - var_R ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
        del_G = ( ( ( var_Max - var_G ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
        del_B = ( ( ( var_Max - var_B ) / 6.0 ) + ( del_Max / 2.0 ) ) / del_Max
        if    var_R == var_Max : h = del_B - del_G
        elif  var_G == var_Max : h = ( 1.0 / 3.0 ) + del_R - del_B
        elif  var_B == var_Max : h = ( 2.0 / 3.0 ) + del_G - del_R
        while h < 0.0: h += 1.0
        while h > 1.0: h -= 1.0
                                        
    return (h,s,l)

def RGBA_to_Hex(color):
    r = int(round(color[0] * 0xFF))
    g = int(round(color[1] * 0xFF))
    b = int(round(color[2] * 0xFF))
    a = int(round(color[3] * 0xFF))
    return (r << 24) + (g << 16) + (b << 8) ++ a


def RGB_to_RGBA(color) :
    return (color[0], color[1], color[2], 1.0)
