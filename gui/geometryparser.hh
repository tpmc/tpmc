// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef GEOMETRYPARSER_HH
#define GEOMETRYPARSER_HH

#include <dune/common/shared_ptr.hh>
#include <dune/common/exceptions.hh>
#include <cctype>
#include <string>
#include <exception>
#include <sstream>
#include <queue>
#include <vector>
#include "geometries.hh"

class ParseException : public Dune::Exception {};

template <char sep>
class GeometryParser {
  enum L_OBJ {
    L_0, L_1, L_2, L_3, L_4, L_5, L_6, L_7, L_8, L_9,
    L_FACE, L_SEP, L_BRACO, L_BRACC
  };
public:
  template <typename ctype, int dim>
  void parse(const std::string& s,
             Geometry::Element<ctype, dim>& result);
private:
  void lex(const std::string& s,
           std::queue<L_OBJ>& result);

  template <typename ctype, int dim>
  void element(Geometry::Element<ctype, dim>& e,
               std::queue<L_OBJ>& l);
  template <typename ctype, int dim>
  Dune::shared_ptr<Geometry::Vertex<ctype, dim> > vertex(std::queue<L_OBJ>& l);
  template <typename ctype, int dim>
  Dune::shared_ptr<Geometry::Vertex<ctype, dim> > point(std::queue<L_OBJ>& l);
  int number(std::queue<L_OBJ>& l);

  bool accept(std::queue<L_OBJ>& l, L_OBJ o);
  void expect(std::queue<L_OBJ>& l, L_OBJ o);
};

template <char sep>
template <typename ctype, int dim>
void GeometryParser<sep>::parse(const std::string& string,
                                Geometry::Element<ctype, dim>& result) {
  std::string s(string);
  s.erase(std::remove_if(s.begin(), s.end(), isspace), s.end());
  std::queue<L_OBJ> lexed;
  lex(s, lexed);
  element(result, lexed);
}

template <char sep>
void GeometryParser<sep>::lex(const std::string& s,
                              std::queue<L_OBJ>& result) {
  std::stringstream ss(s);
  char c;
  while (ss >> c) {
    c = tolower(c);
    switch (c) {
    case '0' : result.push(L_0); break;
    case '1' : result.push(L_1); break;
    case '2' : result.push(L_2); break;
    case '3' : result.push(L_3); break;
    case '4' : result.push(L_4); break;
    case '5' : result.push(L_5); break;
    case '6' : result.push(L_6); break;
    case '7' : result.push(L_7); break;
    case '8' : result.push(L_8); break;
    case '9' : result.push(L_9); break;
    case 'f' : result.push(L_FACE); ss.ignore(3); break;
    case '(' : result.push(L_BRACO); break;
    case ')' : result.push(L_BRACC); break;
    case sep : result.push(L_SEP); break;
    default : DUNE_THROW(ParseException, "illegal char found: " << c);
    }
  }
}

template <char sep>
template <typename ctype, int dim>
void GeometryParser<sep>::element(Geometry::Element<ctype, dim>& e,
                                  std::queue<L_OBJ>& l) {
  Dune::shared_ptr<Geometry::Vertex<ctype, dim> > v = vertex<ctype, dim>(l);
  if (!v)
    DUNE_THROW(ParseException, "element: vertex expected but not found");
  e.add(v);
  while (accept(l, L_SEP)) {
    v = vertex<ctype, dim>(l);
    if (!v)
      DUNE_THROW(ParseException, "element: vertex expected but not found");
    e.add(v);
  }
  if (!l.empty())
    DUNE_THROW(ParseException, "element: list not empty");
}

template <char sep>
template <typename ctype, int dim>
Dune::shared_ptr<Geometry::Vertex<ctype, dim> > GeometryParser<sep>::vertex(std::queue<L_OBJ>& l) {
  if (accept(l, L_BRACO)) {
    Dune::shared_ptr<Geometry::Vertex<ctype, dim> > first = vertex<ctype, dim>(l);
    expect(l, L_SEP);
    Dune::shared_ptr<Geometry::Vertex<ctype, dim> > second = vertex<ctype, dim>(l);
    expect(l, L_BRACC);
    return Dune::shared_ptr<Geometry::Vertex<ctype, dim> >(new Geometry::IntersectionVertex<ctype, dim>(first, second));
  } else {
    return point<ctype, dim>(l);
  }
}

template <char sep>
template <typename ctype, int dim>
Dune::shared_ptr<Geometry::Vertex<ctype, dim> > GeometryParser<sep>::point(std::queue<L_OBJ>& l) {
  if (accept(l, L_FACE)) {
    int i = number(l);
    return Dune::shared_ptr<Geometry::Vertex<ctype, dim> >(new Geometry::FaceVertex<ctype, dim>(i));
  } else {
    int i = number(l);
    return Dune::shared_ptr<Geometry::Vertex<ctype, dim> >(new Geometry::ReferenceVertex<ctype, dim>(i));
  }
}

template <char sep>
int GeometryParser<sep>::number(std::queue<L_OBJ>& l) {
  std::stack<int> s;
  while (!l.empty() && l.front() < 10) {
    s.push(l.front());
    l.pop();
  }
  int result = 0;
  while (!s.empty()) {
    result *= 10;
    result += s.top();
    s.pop();
  }
  return result;
}

template <char sep>
bool GeometryParser<sep>::accept(std::queue<L_OBJ>& l,
                                 L_OBJ o) {
  if (!l.empty() && l.front() == o) {
    l.pop();
    return true;
  }
  return false;
}

template <char sep>
void GeometryParser<sep>::expect(std::queue<L_OBJ>& l,
                                 L_OBJ o) {
  if (!l.empty() && l.front() == o) {
    l.pop();
  } else {
    if (l.empty())
      DUNE_THROW(ParseException, "expect: " << o << " but list is empty");
    else
      DUNE_THROW(ParseException, "expect: " << o << " but " << l.front() << " found");
  }
}

#endif //GEOMETRYPARSER_HH
