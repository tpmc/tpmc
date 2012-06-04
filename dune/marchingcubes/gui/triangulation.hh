// -*- tab-width: 4; indent-tabs-mode: nil; c-basic-offset: 2 -*-
// vi: set et ts=4 sw=2 sts=2:
#ifndef TRIANGULATION_HH
#define TRIANGULATION_HH

/******************************************************************************/
/* VERTEX                                                                     */
/******************************************************************************/

template <typename ctype, int dim>
class Vertex {
public:
  typedef ctype CoordType;
  typedef Dune::FieldVector<CoordType, dim> VectorType;
  Vertex(const VectorType& vertex, const VectorType& normal)
    : mVertex(vertex), mNormal(normal) {}
  const VectorType& vertex() const { return mVertex; }
  const VectorType& normal() const { return mNormal; }
private:
  VectorType mVertex;
  VectorType mNormal;
};

/******************************************************************************/
/* ELEMENT                                                                    */
/******************************************************************************/

template <typename ctype, int dim>
class Element {
public:
  typedef std::size_t SizeType;
  typedef typename Vertex<ctype, dim>::CoordType CoordType;
  typedef typename Vertex<ctype, dim>::VectorType VectorType;
  typedef typename std::vector<Vertex<ctype, dim> >::const_iterator const_iterator;
  void add(const Vertex<ctype, dim>& vertex) { mVertices.push_back(vertex); }
  SizeType size() const { return mVertices.size(); }
  const_iterator begin() const { return mVertices.begin(); }
  const_iterator end() const { return mVertices.end(); }
  const Vertex<ctype, dim>& operator[](SizeType i) const { return mVertices[i]; }
private:
  std::vector<Vertex<ctype, dim> > mVertices;
};



/******************************************************************************/
/* TRIANGULATION                                                              */
/******************************************************************************/

template <typename ctype, int dim>
class Triangulation {
public:
  typedef std::vector<Element<ctype, dim> > ElementContainerType;
  typedef typename ElementContainerType::const_iterator const_iterator;

  void clear() { mElements.clear(); }
  void add(const Element<ctype, dim>& element) { mElements.push_back(element); }
  const_iterator begin() const { return mElements.begin(); }
  const_iterator end() const { return mElements.end(); }
private:
  ElementContainerType mElements;
};

#endif //TRIANGULATION_HH
