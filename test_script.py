from dash import dcc, html
from dash.development.base_component import Component
from app import app

def iter_components(component):
    if isinstance(component, Component):
        yield component
        children = getattr(component, "children", None)
        if isinstance(children, (list, tuple)):
            for child in children:
                yield from iter_components(child)
        elif children is not None:
            yield from iter_components(children)

def test_header_is_present():
    headers = [ component for component in iter_components(app.layout) if isinstance(component, html.H1)]
    assert any(header.children == "Pink Morsel Sales Visualiser" for header in headers)


def test_visualisation_is_present():
    graphs = [component for component in iter_components(app.layout) if isinstance(component, dcc.Graph)]
    assert any(graph.id == "sales-line-chart" for graph in graphs)


def test_region_picker_is_present():
    radio_items = [component for component in iter_components(app.layout) if isinstance(component, dcc.RadioItems)]
    assert any(component.id == "region-filter" for component in radio_items)