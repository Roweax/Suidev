//
//  Math.h
//  suidev_cpp
//
//  Created by Roweax on 2017/7/29.
//  Copyright © 2017年 Roweax. All rights reserved.
//

#ifndef Math_h
#define Math_h


class Vector2 {
public:
    Vector2()
    {
        
    }
    Vector2(double ix, double iy)
    : x(ix)
    , y(iy)
    {
        
    }
    
    double x;
    double y;
};




class Vector3 {
public:
    Vector3()
    {
        
    }
    
    Vector3(const Vector2& ixy, double iz)
    : x(ixy.x)
    , y(ixy.y)
    , z(iz)
    {
        
    }
    
    Vector3(double ix, double iy, double iz)
    : x(ix)
    , y(iy)
    , z(iz)
    {
        
    }
    
    Vector3 operator + (const Vector3& other) const  {
        return Vector3(this->x + other.x, this->y + other.y, this->z + other.z);
    }
    
    Vector3 operator - (const Vector3& other) const {
        return Vector3(this->x - other.x, this->y - other.y, this->z - other.z);
    }
    
    Vector3 operator * (double other) const {
        return Vector3(this->x * other, this->y * other, this->z * other);
    }
    
    Vector3 operator / (double other) const {
        return Vector3(this->x / other, this->y / other, this->z / other);
    }
    
    double x;
    double y;
    double z;
};


#endif /* Math_h */
