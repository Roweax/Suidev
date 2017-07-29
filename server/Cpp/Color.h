//
//  Color.h
//  suidev_cpp
//
//  Created by Roweax on 2017/7/29.
//  Copyright © 2017年 Roweax. All rights reserved.
//

#ifndef Color_h
#define Color_h

class ColorRGB {
public:
    ColorRGB() {
        
    }
    
    ColorRGB(double ir, double ig, double ib)
    : r(ir)
    , g(ig)
    , b(ib) {
        
    }
    
    double r;
    double g;
    double b;
};

class ColorHSL {
public:
    ColorHSL() {
        
    }
    ColorHSL(double ih, double is, double il)
    : h(ih)
    , s(is)
    , l(il) {
        
    }
    double h;
    double s;
    double l;
};


class Color {
public:
    static ColorHSL RGBToHSL(const ColorRGB &rgb) {
        double h = 0, s = 0, l = 0;
        double r = rgb.r;
        double g = rgb.g;
        double b = rgb.b;
        
        double max = Max(r, Max(g, b));
        double min = Min(r, Min(g, b));
        
        // hue
        if (max == min) {
            h = 0; // undefined
        }
        else if (max == r && g >= b) {
            h = 60.0 * (g - b) / (max - min);
        }
        else if (max == r && g < b) {
            h = 60.0 * (g - b) / (max - min) + 360.0;
        }
        else if (max == g) {
            h = 60.0 * (b - r) / (max - min) + 120.0;
        }
        else if (max == b) {
            h = 60.0 * (r - g) / (max - min) + 240.0;
        }
        
        // luminance
        l = (max + min) / 2.0;
        
        // saturation
        if (l == 0 || max == min) {
            s = 0;
        }
        else if (0 < l && l <= 0.5) {
            s = (max - min) / (max + min);
        }
        else if (l > 0.5) {
            s = (max - min) / (2 - (max + min)); //(max-min > 0)?
        }
        return ColorHSL(h, s, l);
    }
    
    
    static ColorRGB HSLToRGB(const ColorHSL &hsl) {
        double h = hsl.h;
        double s = hsl.s;
        double l = hsl.l;
        if (s == 0) {
            return ColorRGB(l, l, l);
        }
        else {
            double q = (l < 0.5) ? (l * (1.0 + s)) : (l + s - (l * s));
            double p = (2.0 * l) - q;
            
            double Hk = h / 360.0;
            double T[3];
            T[0] = Hk + (1.0 / 3.0);    // Tr
            T[1] = Hk;                  // Tb
            T[2] = Hk - (1.0 / 3.0);    // Tg
            
            for (int i = 0; i < 3; i++) {
                if (T[i] < 0) {
                    T[i] += 1.0;
                }
                if (T[i] > 1) {
                    T[i] -= 1.0;
                }
                
                if ((T[i] * 6) < 1) {
                    T[i] = p + ((q - p) * 6.0 * T[i]);
                }
                else if ((T[i] * 2.0) < 1) {
                    T[i] = q;
                }
                else if ((T[i] * 3.0) < 2) {
                    T[i] = p + (q - p) * ((2.0 / 3.0) - T[i]) * 6.0;
                }
                else {
                    T[i] = p;
                }
            }
            return ColorRGB(T[0], T[1], T[2]);
        }
        
    }
};

#endif /* Color_h */
