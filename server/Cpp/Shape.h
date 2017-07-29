//
//  Cube.h
//  suidev_cpp
//
//  Created by Roweax on 2017/7/29.
//  Copyright © 2017年 Roweax. All rights reserved.
//

#ifndef Cube_h
#define Cube_h

#include "Color.h"
#include "Math.h"

enum Material {
    LEGO,
    GLASS,
    LED,
    METAL,
    SUBSURFACE
};

class Cube {
public:
    Cube()
    {
        
    }
    Cube(const Vector3& ipos, const Vector3 &isize)
    : position(ipos)
    , size(isize)
    , material(LEGO)
    {
        
    }
    
    Vector3 position;
    Vector3 size;
    ColorRGB color;
    Material material;
};



#endif /* Cube_h */
