//
//  UBatch.h
//  suidev_cpp
//
//  Created by Roweax on 2017/7/20.
//  Copyright © 2017年 Roweax. All rights reserved.
//

#ifndef UBatch_h
#define UBatch_h

#include <functional>
#include <vector>
#include <math.h>
#include <algorithm>

template<class T> static inline T Max(T x, T y) { return x > y ? x : y; }
template<class T> static inline T Min(T x, T y) { return x < y ? x : y; }


// lambda
template <class T>
class UTraits : public UTraits<decltype(&T::operator())> {
};


// base
template <class ClassType, class RT, class ... ATS>
class UTraits<RT(ClassType::*)(ATS...) const> {
public:
    static const size_t ArgsCount = sizeof ...(ATS);
    typedef RT ReturnType;
    typedef RT FunctionType(ATS ...);
    
    template<size_t I>
    class Args {
    public:
        static_assert(I < ArgsCount, "Arg index is out of range!");
        typedef typename std::tuple_element<I, std::tuple<ATS...>>::type Type;
    };
};


// normal funtion pointer
template <class RT, class ... ATS>
class UTraits<RT(*)(ATS...)> : UTraits<RT(ATS...)> {
};


// std::function
template <class RT, class ... ATS>
class UTraits<std::function<RT(ATS...)>> : UTraits<RT(ATS...)> {
};



template <class ElementType>
class UBatch {
public:
    typedef ElementType ValueType;
    
    template <class FunctionType>
    using UBatchReturn = UBatch<typename UTraits<FunctionType>::ReturnType>;
    
    template <class FunctionType>
    using UReturn = typename UTraits<FunctionType>::ReturnType;
    
    class Iterator {
    public:
        Iterator(UBatch* owner, int index)
        : m_Owner(owner)
        , m_Index(index) {
            
        }
        
        bool operator==(const Iterator & x) const {
            return m_Index == x.m_Index;
        }
        
        
        bool operator!=(const Iterator & x) const {
            return !(*this == x);
        }
        
        
        ElementType& operator*() const {
            return m_Owner->Get(m_Index);
        }
        
        ElementType* operator->() const {
            return &m_Owner->Get(m_Index);
        }
        
        
        bool IsValid() const {
            return m_Index >= 0 && m_Index < m_Owner->Count();
        }
        
        
        Iterator& operator++() {
            m_Index++;
            return *this;
        }
        
        
        Iterator operator++(int) {
            Iterator tmp = *this;
            ++*this;
            return tmp;
        }
        
        
        Iterator& operator--() {
            m_Index--;
            return *this;
        }
        
        
        Iterator operator--(int) {
            Iterator tmp = *this;
            --*this;
            return tmp;
        }
        //operator T*() const{return m_Owner->Get(m_Index);}
    private:
        UBatch*     m_Owner;
        int         m_Index;
    };
    
    
    class ConstIterator {
    public:
        ConstIterator(const UBatch* owner, bool index)
        : m_Owner(owner)
        , m_Index(index) {
            
        }
        
        
        bool operator==(const Iterator & x) const {
            return m_Index == x.m_Index;
        }
        
        
        bool operator!=(const Iterator & x) const {
            return !(*this == x);
        }
        
        const ElementType& operator*() const {
            return m_Owner->Get(m_Index);
        }
        
        
        const ElementType* operator->() const {
            return &m_Owner->Get(m_Index);
        }
        
        
        bool IsValid() const {
            return m_Index >= 0 && m_Index < m_Owner->Count();
        }
        
        
        ConstIterator& operator++() {
            m_Index++;
            return *this;
        }
        
        
        ConstIterator operator++(int) {
            ConstIterator tmp = *this;
            ++*this;
            return tmp;
        }
        
        
        ConstIterator& operator--() {
            m_Index--;
            return *this;
        }
        
        
        ConstIterator operator--(int) {
            Iterator tmp = *this;
            --*this;
            return tmp;
        }
        //operator T*() const{return m_Owner->Get(m_Index);}
    private:
        const UBatch*   m_Owner;
        int             m_Index;
    };
    
    
    UBatch() {
        
    }
    
    template <class ElementA, class ElementB>
    UBatch(const UBatch<ElementA> &BatchA, const UBatch<ElementB> &BatchB) {
        *this = CombinByOneMax(BatchA, BatchB, [](const ElementA &a, const ElementB &b) {return ElementType(a, b); });
    }
    
    
    UBatch(int count)
    : m_Data(count) {
        
    }
    
    
    UBatch(int size, ElementType value)
    : m_Data(size, value) {
        
    }
    
    
    template<class Function>
    UBatch(int count, const Function &function)
    : m_Data(count) {
        for (int i = 0; i < m_Data.size(); ++i) {
            m_Data[i] = function(i);
        }
    }
    
    
    UBatch(int size, const ElementType& start, const ElementType& step)
    : m_Data(size) {
        ElementType cur = start;
        for (int i = 0; i < m_Data.size(); ++i) {
            m_Data[i] = cur;
            cur += step;
        }
    }
    
    
    void AddItem(const ElementType &value) {
        m_Data.push_back(value);
    }
    
    void Add(const UBatch<ElementType>  &other) {
        for (int i = 0; i < other.Count(); ++i) {
            m_Data.push_back(other[i]);
        }
    }
    
    const ElementType& Get(int index) const {
        return m_Data[index % m_Data.size()];
    }
    
    
    int Count() const {
        return m_Data.size();
    }
    
    /*
     UString ToString() const {
     UString result = "{";
     for (s32 i = 0; i < Count(); ++i) {
     if(i > 0) {
     result += ", ";
     }
     result += UWrapObject<ElementType>(Get(i)).ToString();
     }
     result += "}";
     return result;
     }*/
    template<class Function>
    UBatch& Call(const Function &function) {
        for (int i = 0; i < Count(); ++i) {
            function(m_Data[i]);
        }
        return *this;
    }
    
    template<class Function>
    UReturn<Function> Each(const Function &function) const {
        UReturn<Function> result;
        for (int i = 0; i < Count(); ++i) {
            result.Add(function(m_Data[i]));
        }
        return result;
    }
    
    template<class Function>
    UBatchReturn<Function> Select(const Function &function) const {
        UBatchReturn<Function> result(Count());
        for (int i = 0; i < Count(); ++i) {
            result[i] = function(m_Data[i]);
        }
        return result;
    }
    
    
    template<class Function>
    UBatch<ElementType> Where(const Function &function) const {
        UBatch<ElementType> result;
        for (int i = 0; i < Count(); ++i) {
            if (function(m_Data[i])) {
                result.m_Data.push_back(m_Data[i]);
            }
        }
        return result;
    }
    
    
    UBatch<ElementType> Union(const UBatch<ElementType> &other) {
        UBatch<ElementType> result = *this;
        for (int i = 0; i < other.Count(); ++i) {
            result.m_Data.push_back(other[i]);
        }
        return result;
    }
    
    
    template<class ElementA, class ElementB, class Function>
    static UBatchReturn<Function> CombinByOneMin(const UBatch<ElementA> &a, const UBatch<ElementB> &b, const Function& func) {
        int count = min(a.Count(), b.Count());
        UBatchReturn<Function> result(count);
        int  m = 0;
        for (int i = 0; i < count; ++i) {
            result[m++] = func(a.Get(i), b.Get(i));
        }
        return result;
    }
    
    
    template<class Function>
    static UBatch CombinByOneMin(const UBatch &a, const UBatch &b, const UBatch &c, const Function& func) {
        
    }
    
    
    template<class ElementA, class ElementB, class Function>
    static UBatchReturn<Function> CombinByOneMax(const UBatch<ElementA> &a, const UBatch<ElementB> &b, const Function& func) {
        int count = Max(a.Count(), b.Count());
        UBatchReturn<Function> result(count);
        int  m = 0;
        for (int i = 0; i < count; ++i) {
            result[m++] = func(a.Get(i), b.Get(i));
        }
        return result;
    }
    
    
    template<class Function>
    static UBatch CombinByOneMax(const UBatch &a, const UBatch &b, const UBatch &c, const Function& func) {
        
    }
    
    
    template<class ElementA, class ElementB, class Function>
    static UBatchReturn<Function> CombinByEach(const UBatch<ElementA> &a, const UBatch<ElementB> &b, const Function& func) {
        int count = a.Count() * b.Count();
        UBatchReturn<Function> result(count);
        int  m = 0;
        for (int i = 0; i < a.Count(); ++i) {
            for (int j = 0; j < b.Count(); ++j) {
                result[m++] = func(a[i], b[j]);
            }
        }
        return result;
    }
    
    
    template<class ElementA, class ElementB, class ElementC, class Function>
    static UBatchReturn<Function> CombinByEach(const UBatch<ElementA> &a, const UBatch<ElementB> &b, const UBatch<ElementC> &c, const Function& func) {
        int count = a.Count() * b.Count() * c.Count();
        UBatchReturn<Function> result(count);
        int  m = 0;
        for (int i = 0; i < a.Count(); ++i) {
            for (int j = 0; j < b.Count(); ++j) {
                for (int k = 0; k < c.Count(); ++k) {
                    result[m++] = func(a[i], b[j], c[k]);
                }
            }
        }
        return result;
    }
    
    
    Iterator Begin() {
        return Iterator(this, 0);
    }
    
    
    ConstIterator Begin() const {
        return ConstIterator(this, 0);
    }
    
    
    UBatch operator + (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {return a + b; });
    }
    
    
    UBatch operator - (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {return a - b; });
    }
    
    
    UBatch operator * (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {return a * b; });
    }
    
    
    UBatch operator / (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {return a / b; });
    }
    
    
    UBatch<bool> operator == (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {
            return a == b;
        });
    }
    
    
    UBatch<bool> operator > (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {
            return a > b;
        });
    }
    
    
    UBatch<bool> operator < (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {
            return a < b;
        });
    }
    
    
    UBatch<bool> operator >= (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {
            return a >= b;
        });
    }
    
    
    UBatch<bool> operator <= (const UBatch &other) const {
        return CombinByOneMax(*this, other, [](const ElementType &a, const ElementType &b) {
            return a <= b;
        });
    }
    
    
    ElementType& operator[](int index) {
        return m_Data[index];
    }
    
    
    const ElementType& operator[](int index) const {
        return m_Data[index];
    }
    
    
    operator bool() const {
        for (auto it = Begin(); it.IsValid(); it++) {
            if (b8(*it) == false) {
                return false;
            }
        }
        return true;
    }
    
private:
    std::vector<ElementType>         m_Data;
};

#endif /* UBatch_h */
