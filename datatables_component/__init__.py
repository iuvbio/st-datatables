import os
import streamlit.components.v1 as components

# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = False

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "datatables_component",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component(
        "datatables_component", path=build_dir
    )


# Create a wrapper function for the component. This is an optional
# best practice - we could simply expose the component function returned by
# `declare_component` and call it done. The wrapper allows us to customize
# our component's API: we can pre-process its input args, post-process its
# output value, and add a docstring for users.
def datatables_component(df, key=None):
    """Create a new instance of "datatables_component".

    Parameters
    ----------
    name: str
        The name of the thing we're saying hello to. The component will display
        the text "Hello, {name}!"
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    int
        The number of times the component's "Click Me" button has been clicked.
        (This is the value passed to `Streamlit.setComponentValue` on the
        frontend.)

    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    tabledata = df.to_dict(orient="records")
    columns = [{"data": key} for key in df.columns.tolist()]
    component_value = _component_func(
        tabledata=tabledata, columns=columns, key=key, default=None
    )

    # components.html(
    #    """
    #    <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.11.3/css/jquery.dataTables.css">
    #    <script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
    #    <script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.11.3/js/jquery.dataTables.js"></script>
    #    <script>
    #      $(document).ready(function() {{
    #          $('#datatables-table').DataTable({{
    #            data: {},
    #            columns: {}
    #          }});
    #      }} );
    #    </script>
    #      <body>
    #        <noscript>You need to enable JavaScript to run this app.</noscript>
    #        <table id="datatables-table">
    #          <thead>
    #            <tr>
    #              <th>a</th>
    #              <th>b</th>
    #              <th>c</th>
    #              <th>d</th>
    #            </tr>
    #          </thead>
    #        </table>
    #      </body>
    #    """.format(
    #        tabledata, columns
    #    ),
    #    height=600,
    # )
    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


# Add some test code to play with the component while it's in development.
# During development, we can run this just as we would any other Streamlit
# app: `$ streamlit run datatables_component/__init__.py`
if not _RELEASE:
    from string import ascii_letters

    import numpy as np
    import pandas as pd
    import streamlit as st

    df = pd.DataFrame(
        {
            "a": np.random.choice(list(ascii_letters), size=20),
            "b": np.random.randint(0, 10, 20),
            "c": np.random.randint(0, 100, 20),
            "d": np.random.randint(-200, 200, 20),
        }
    )

    st.subheader("Component with constant args")

    # Create a second instance of our component whose `name` arg will vary
    # based on a text_input widget.
    #
    # We use the special "key" argument to assign a fixed identity to this
    # component instance. By default, when a component's arguments change,
    # it is considered a new instance and will be re-mounted on the frontend
    # and lose its current state. In this case, we want to vary the component's
    # "name" argument without having it get recreated.
    # st.markdown(df.to_html(table_id=table_id), unsafe_allow_html=True)
    _ = datatables_component(df, key="foo")
