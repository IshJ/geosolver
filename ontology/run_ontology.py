"""
For local running, including testing.
"""

from geosolver.ontology.augment_ontology import augment_ontology
from geosolver.text.semantics.costs.get_ontology_path_cost import get_ontology_path_cost
from geosolver.ontology.get_ontology_paths import get_ontology_paths
from geosolver.ontology.states import Function
from geosolver.ontology import basic_ontology

__author__ = 'minjoon'


def test_load_ontology():
    o = basic_ontology
    print(o.inheritance_graph.edges())
    print(o.ontology_graph.edges(data=True))
    print(o.isinstance(o.types['triangle'], o.types['polygon']))
    # o.display_ontology_graph()
    t = o.types['number']
    print(o.isinstance(t, t))


def test_get_ontology_path_cost():
    """
    Needs to be moved to semantics package.
    :return:
    """
    o = basic_ontology
    s0 = Function('5', [], o.types['number'])
    s1 = Function('AB', [], o.types['reference'])
    oo = augment_ontology(o, {s0.name: s0, s1.name: s1})
    s2 = o.functions['equal']
    s3 = o.functions['radiusOf']
    s4 = o.functions['isRadiusOf']
    s5 = o.functions['circle']
    truth = o.types['truth']
    number = o.types['number']
    perp = oo.functions['isPerpendicularTo']
    line = o.types['line']
    cf = o.functions['circle']
    paths = get_ontology_paths(oo, truth, s1)
    for path in paths.values():
        print(path)
        print(get_ontology_path_cost(path))


if __name__ == "__main__":
    test_load_ontology()
    # test_augment_ontology()
