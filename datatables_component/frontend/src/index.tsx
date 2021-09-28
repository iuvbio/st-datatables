import { Streamlit, RenderData } from "streamlit-component-lib"
import 'datatables.net'
import 'datatables.net-dt/css/jquery.dataTables.css';
import 'datatables.net-buttons-dt/css/buttons.dataTables.css';
var $       = require( 'jquery' );
//var dt      = require( 'datatables.net' )();
//var buttons = require( 'datatables.net-buttons' )();

const span = document.body.appendChild(document.createElement("span"))
const table = document.createElement("table")

function makeid(length: number): string {
  var result           = '';
  var characters       = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  var charactersLength = characters.length;
  for ( var i = 0; i < length; i++ ) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
  }
  return `datatable-${result}`;
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event: Event): void {
  // Get the RenderData from the event
  const data = (event as CustomEvent<RenderData>).detail

  // RenderData.args is the JSON dictionary of arguments sent from the
  // Python script.
  let tabledata = data.args["tabledata"]
  let columns = data.args["columns"]
  console.log(tabledata)
  console.log(columns)

  const table_id = makeid(10)
  table.setAttribute("id", table_id)
  table.setAttribute("class", "display")
  const thead = table.appendChild(document.createElement("thead"))
  const trow = thead.appendChild(document.createElement("tr"))
  for (let c of Object.keys(columns)) {
    const th = trow.appendChild(document.createElement("th"))
    th.textContent = c
  }
  span.appendChild(table)
  span.appendChild(document.createElement("br"))

  $(`#${table_id}`).DataTable({
    data: tabledata,
    columns: columns
  });

  // We tell Streamlit to update our frameHeight after each render event, in
  // case it has changed. (This isn't strictly necessary for the example
  // because our height stays fixed, but this is a low-cost function, so
  // there's no harm in doing it redundantly.)
  Streamlit.setFrameHeight()
}

// Attach our `onRender` handler to Streamlit's render event.
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)

// Tell Streamlit we're ready to start receiving data. We won't get our
// first RENDER_EVENT until we call this function.
Streamlit.setComponentReady()

// Finally, tell Streamlit to update our initial height. We omit the
// `height` parameter here to have it default to our scrollHeight.
Streamlit.setFrameHeight()
