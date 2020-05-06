import React from "react";
import "./App.css";
import Page from "./Components";
import { Query, getPartsForQuery, getUrlForQuery } from "./Query";
let controller;

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      model: props.model,
      fields: props.fields,
      filters: props.filters,
      data: [],
    };
  }

  fetchData(state) {
    const url = getUrlForQuery(this.props.baseUrl, state, "json");

    if (controller) controller.abort();
    controller = new AbortController();

    fetch(url, { signal: controller.signal })
      .then((res) => res.json())
      .then(
        (result) => {
          this.setState(result);
        },
        (error) => {
          this.setState({
            error,
          });
        }
      );
  }

  componentDidMount() {
    const reqState = {
      model: this.state.model,
      fields: this.state.fields,
      filters: this.state.filters,
    };
    window.history.replaceState(
      reqState,
      null,
      getUrlForQuery(this.props.baseUrl, this.state, "html")
    );
    this.fetchData(this.state);
    window.onpopstate = (e) => {
      console.log("popstate", e.state);
      this.fetchData(e.state);
    };
  }

  handleQueryChange(queryChange) {
    const newState = { ...this.state, ...queryChange };
    this.setState(queryChange);
    const reqState = {
      model: newState.model,
      fields: newState.fields,
      filters: newState.filters,
    };
    window.history.pushState(
      reqState,
      null,
      getUrlForQuery(this.props.baseUrl, newState, "html")
    );
    this.fetchData(newState);
  }

  render() {
    return (
      <Page
        query={new Query(this.props, this.state, this.handleQueryChange.bind(this))}
        sortedModels={this.props.sortedModels}
        {...this.state}
      />
    );
  }
}

export default App;
