// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef ISDEGENERATED_HH
#define ISDEGENERATED_HH

/** \file
 * \brief Code to detect degenerate elements
 */

#include <dune/common/fvector.hh>

namespace Dune {
  template <class ctype>
  struct IsDegeneratedBase {

    /** \brief Return true if a and b differ by less than 1e-8 in the 1-norm */
    template<int dim>
    static bool eq(const FieldVector<ctype,dim> & a,
                   const FieldVector<ctype,dim> & b)
    {
      static const ctype eqEpsilon = 1e-8;
      ctype sum = 0;
      for (int d=0; d<dim; d++)
        sum += std::abs(a[d] - b[d]);
      return (sum <= eqEpsilon);
    }
  };

  template <class ctype, int dim>
  struct IsDegenerated {
    typedef FieldVector<ctype,dim> Point;
    template<int d>
    static bool check (std::vector< FieldVector<ctype,d> > & c) {
      return false;
    }
  };

  template <class ctype>
  struct IsDegenerated<ctype, 0> : IsDegeneratedBase<ctype> {
    enum { dim = 0 };
    template<int d>
    static bool check (std::vector< FieldVector<ctype,d> > & c) {
      return true;
    }
  };

  template <class ctype>
  struct IsDegenerated<ctype, 1> : IsDegeneratedBase<ctype> {
    enum { dim = 1 };
    template<int d>
    static bool check (std::vector< FieldVector<ctype,d> > & c) {
      return eq(c[0],c[1]);
    }
  };

  /** \brief Specialization for 2d elements */
  template <class ctype>
  struct IsDegenerated<ctype, 2> : IsDegeneratedBase<ctype> {
    enum { dim = 2 };

    /** \brief Delete the entry with number 'pos' from the vector 'c'
     * \todo Why not just call c.erase(c.begin()+pos) instead?
     */
    template<int d>
    static void erase (int pos, std::vector< FieldVector<ctype,d> > & c) {
      for (size_t i=pos; i<c.size()-1; i++) c[i] = c[i+1];
      c.pop_back();
    }


    /** \brief Return true if the triangle or quadrilateral with corners given by 'c' is degenerate */
    template<int d>
    static bool check (std::vector< FieldVector<ctype,d> > & c) {
      switch (c.size())
      {
      case 3 :
        return (eq(c[0],c[1]) || eq(c[0],c[2]) || eq(c[1],c[2]) );
      case 4 :
        if (eq(c[0],c[1])) { erase(1,c); return check(c); }
        if (eq(c[0],c[2])) { erase(2,c); return check(c); }
        if (eq(c[0],c[3])) { return true; }
        if (eq(c[1],c[2])) { return true; }
        if (eq(c[1],c[3])) { erase(3,c); return check(c); }
        if (eq(c[2],c[3])) { erase(3,c); return check(c); }
        return ( (eq(c[0],c[1]) && eq(c[2],c[3])) ||
                 (eq(c[0],c[2]) && eq(c[1],c[3])) );
      default :
        DUNE_THROW(Dune::Exception, "Impossible Geometry. " <<
                   "In 2D there is no known geometry with " <<
                   c.size() << " corners");
      }
    }
  };

  /** \brief Specialization for 3d elements */
  template <class ctype>
  struct IsDegenerated<ctype, 3> : IsDegeneratedBase<ctype> {
    enum { dim = 3 };

    /** \brief Return true if the element with the corners given by 'c' is degenerate */
    template<int d>
    static bool check (std::vector< FieldVector<ctype,d> > & c) {
      switch (c.size())
      {
      case 4 :
        return ( eq(c[0],c[1]) ||
                 eq(c[0],c[2]) ||
                 eq(c[0],c[3]) ||
                 eq(c[1],c[2]) ||
                 eq(c[1],c[3]) ||
                 eq(c[2],c[3]));
      case 5 :
      {
        bool deg=false;
        deg |= eq(c[3],c[0]);
        deg |= eq(c[2],c[1]);
        int mat(0);
        mat += int(eq(c[0],c[1]));
        mat += int(eq(c[0],c[2]));
        mat += int(eq(c[0],c[4]));
        mat += int(eq(c[1],c[3]));
        mat += int(eq(c[1],c[4]));
        mat += int(eq(c[2],c[3]));
        mat += int(eq(c[2],c[4]));
        mat += int(eq(c[3],c[4]));
        return deg || mat > 1;
      }
      case 6 :
        return ( (eq(c[0],c[3]) && eq(c[1],c[4]) && eq(c[2],c[5])) ||
                 (eq(c[0],c[1]) && eq(c[3],c[4])) ||
                 (eq(c[0],c[2]) && eq(c[3],c[5])) ||
                 (eq(c[1],c[2]) && eq(c[4],c[5])) );
      case 8 :
        return ( (eq(c[0],c[1]) && eq(c[2],c[3]) && eq(c[4],c[5]) && eq(c[6],c[7])) ||
                 (eq(c[0],c[2]) && eq(c[1],c[3]) && eq(c[4],c[6]) && eq(c[5],c[7])) ||
                 (eq(c[0],c[4]) && eq(c[1],c[5]) && eq(c[2],c[6]) && eq(c[3],c[7])) );
      default :
        DUNE_THROW(Dune::Exception, "Impossible Geometry. " <<
                   "In 3D there is no known geometry with " <<
                   c.size() << " corners");
      }
    }
  };

}

#endif // ISDEGENERATED_HH
