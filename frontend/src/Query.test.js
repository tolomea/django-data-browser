import { Query, getPartsForQuery, getRelUrlForQuery, getUrlForQuery, empty } from "./Query";

// ---- Fixture data ----

const config = {
  baseUrl: "/data-browser/",
  defaultRowLimit: 1000,
  types: {
    string: {
      defaultLookup: "equals",
      defaultValue: "",
      lookups: {
        equals: { type: "string" },
        not_equals: { type: "string" },
        contains: { type: "string" },
        is_null: { type: "boolean" },
      },
    },
    number: {
      defaultLookup: "equals",
      defaultValue: 0,
      lookups: {
        equals: { type: "number" },
        gt: { type: "number" },
        lt: { type: "number" },
      },
    },
    boolean: {
      defaultLookup: "equals",
      defaultValue: true,
      lookups: {
        equals: { type: "boolean" },
      },
    },
  },
  allModelFields: {
    Author: {
      defaultFilters: [],
      fields: {
        name: {
          model: null,
          type: "string",
          canPivot: true,
          concrete: true,
          real: true,
          verboseName: "name",
          toMany: false,
          choices: [],
        },
        book_count: {
          model: null,
          type: "number",
          canPivot: false,
          concrete: true,
          real: true,
          verboseName: "book count",
          toMany: false,
          choices: [],
        },
        books: {
          model: "Book",
          type: null,
          canPivot: true,
          concrete: true,
          real: true,
          verboseName: "books",
          toMany: true,
          choices: [],
        },
      },
    },
    Book: {
      defaultFilters: [{ pathStr: "title", lookup: "equals", value: "" }],
      fields: {
        title: {
          model: null,
          type: "string",
          canPivot: true,
          concrete: true,
          real: true,
          verboseName: "title",
          toMany: false,
          choices: [],
        },
        year: {
          model: null,
          type: "number",
          canPivot: true,
          concrete: true,
          real: true,
          verboseName: "year",
          toMany: false,
          choices: [],
        },
      },
    },
  },
};

const baseQuery = {
  model: "Author",
  fields: [],
  filters: [],
  limit: 100,
  rows: [{}],
  cols: [{}],
  body: [[{}]],
};

function makeQ(queryOverrides = {}) {
  const setQuery = jest.fn();
  const q = { ...baseQuery, ...queryOverrides };
  return { query: new Query(config, q, setQuery), setQuery };
}

// ---- getPartsForQuery ----

describe("getPartsForQuery", () => {
  it("handles an empty query", () => {
    const result = getPartsForQuery({
      model: "Author",
      fields: [],
      filters: [],
      limit: 100,
    });
    expect(result).toEqual({ model: "Author", fields: "", query: "", limit: 100 });
  });

  it("serializes a field with no sort", () => {
    const fields = [{ pathStr: "name", sort: null, priority: null, pivoted: false }];
    const { fields: out } = getPartsForQuery({ model: "Author", fields, filters: [], limit: 100 });
    expect(out).toBe("name");
  });

  it("serializes a field with asc sort and priority", () => {
    const fields = [{ pathStr: "name", sort: "asc", priority: 0, pivoted: false }];
    const { fields: out } = getPartsForQuery({ model: "Author", fields, filters: [], limit: 100 });
    expect(out).toBe("name+0");
  });

  it("serializes a field with dsc sort and priority", () => {
    const fields = [{ pathStr: "name", sort: "dsc", priority: 2, pivoted: false }];
    const { fields: out } = getPartsForQuery({ model: "Author", fields, filters: [], limit: 100 });
    expect(out).toBe("name-2");
  });

  it("serializes a pivoted field with & prefix", () => {
    const fields = [{ pathStr: "name", sort: null, priority: null, pivoted: true }];
    const { fields: out } = getPartsForQuery({ model: "Author", fields, filters: [], limit: 100 });
    expect(out).toBe("&name");
  });

  it("joins multiple fields with commas", () => {
    const fields = [
      { pathStr: "name", sort: "asc", priority: 0, pivoted: false },
      { pathStr: "book_count", sort: null, priority: null, pivoted: false },
    ];
    const { fields: out } = getPartsForQuery({ model: "Author", fields, filters: [], limit: 100 });
    expect(out).toBe("name+0,book_count");
  });

  it("serializes a filter as pathStr__lookup=value", () => {
    const filters = [{ pathStr: "name", lookup: "equals", value: "Alice" }];
    const { query } = getPartsForQuery({ model: "Author", fields: [], filters, limit: 100 });
    expect(query).toBe("name__equals=Alice");
  });

  it("url-encodes special characters in filter values", () => {
    const filters = [{ pathStr: "name", lookup: "contains", value: "a&b=c" }];
    const { query } = getPartsForQuery({ model: "Author", fields: [], filters, limit: 100 });
    expect(query).toBe("name__contains=a%26b%3Dc");
  });

  it("joins multiple filters with &", () => {
    const filters = [
      { pathStr: "name", lookup: "equals", value: "Alice" },
      { pathStr: "book_count", lookup: "gt", value: "5" },
    ];
    const { query } = getPartsForQuery({ model: "Author", fields: [], filters, limit: 100 });
    expect(query).toBe("name__equals=Alice&book_count__gt=5");
  });
});

// ---- getRelUrlForQuery ----

describe("getRelUrlForQuery", () => {
  it("builds the expected relative URL", () => {
    const q = {
      model: "Author",
      fields: [{ pathStr: "name", sort: null, priority: null, pivoted: false }],
      filters: [],
      limit: 100,
    };
    expect(getRelUrlForQuery(q, "json")).toBe("query/Author/name.json?&limit=100");
  });

  it("includes filter string in the URL", () => {
    const q = {
      model: "Author",
      fields: [],
      filters: [{ pathStr: "name", lookup: "equals", value: "Alice" }],
      limit: 50,
    };
    expect(getRelUrlForQuery(q, "csv")).toBe(
      "query/Author/.csv?name__equals=Alice&limit=50"
    );
  });
});

// ---- getUrlForQuery ----

describe("getUrlForQuery", () => {
  it("prepends window.location.origin and the base URL", () => {
    const q = { model: "Author", fields: [], filters: [], limit: 100 };
    const url = getUrlForQuery("/data-browser/", q, "json");
    expect(url).toMatch(/^http:\/\/localhost\/data-browser\//);
    expect(url).toContain("query/Author/");
  });
});

// ---- Query.getField ----

describe("Query.getField", () => {
  it("returns a top-level field", () => {
    const { query } = makeQ();
    expect(query.getField("name")).toBe(config.allModelFields.Author.fields.name);
  });

  it("follows a nested path across models", () => {
    const { query } = makeQ();
    expect(query.getField("books__title")).toBe(
      config.allModelFields.Book.fields.title
    );
  });

  it("returns null for an unknown field", () => {
    const { query } = makeQ();
    expect(query.getField("nonexistent")).toBeNull();
  });

  it("returns null when intermediate path segment is unknown", () => {
    const { query } = makeQ();
    expect(query.getField("nonexistent__title")).toBeNull();
  });
});

// ---- Query.addField ----

describe("Query.addField", () => {
  it("adds a field with no sort", () => {
    const { query, setQuery } = makeQ();
    query.addField("name", null);
    expect(setQuery).toHaveBeenCalledWith({
      fields: [{ pathStr: "name", sort: null, priority: null, pivoted: false }],
    });
  });

  it("adds a field with sort, assigning priority 0 when no other sorted fields", () => {
    const { query, setQuery } = makeQ();
    query.addField("name", "asc");
    expect(setQuery).toHaveBeenCalledWith({
      fields: [{ pathStr: "name", sort: "asc", priority: 0, pivoted: false }],
    });
  });

  it("assigns the next priority when other sorted fields exist", () => {
    const { query, setQuery } = makeQ({
      fields: [{ pathStr: "name", sort: "asc", priority: 0, pivoted: false }],
    });
    query.addField("book_count", "asc");
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields[1].priority).toBe(1);
  });

  it("removes an existing field with the same pathStr before adding", () => {
    const { query, setQuery } = makeQ({
      fields: [{ pathStr: "name", sort: "asc", priority: 0, pivoted: false }],
    });
    query.addField("name", null);
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields).toHaveLength(1);
    expect(fields[0].sort).toBeNull();
  });
});

// ---- Query.removeField ----

describe("Query.removeField", () => {
  it("removes the specified field", () => {
    const field = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const other = { pathStr: "book_count", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [field, other] });
    query.removeField(field);
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields).toHaveLength(1);
    expect(fields[0].pathStr).toBe("book_count");
  });
});

// ---- Query.moveField ----

describe("Query.moveField", () => {
  it("moves a row field right", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const booksField = { pathStr: "books", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [nameField, booksField] });
    query.moveField(nameField, false);
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields[0].pathStr).toBe("books");
    expect(fields[1].pathStr).toBe("name");
  });

  it("moves a row field left", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const booksField = { pathStr: "books", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [nameField, booksField] });
    query.moveField(booksField, true);
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields[0].pathStr).toBe("books");
    expect(fields[1].pathStr).toBe("name");
  });

  it("does nothing when moving left from the first position", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [nameField] });
    query.moveField(nameField, true);
    expect(setQuery).not.toHaveBeenCalled();
  });

  it("does nothing when moving right from the last position", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [nameField] });
    query.moveField(nameField, false);
    expect(setQuery).not.toHaveBeenCalled();
  });
});

// ---- Query.toggleSort ----

describe("Query.toggleSort", () => {
  it("cycles null → asc with priority 0", () => {
    const field = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [field] });
    query.toggleSort(field);
    const newField = setQuery.mock.calls[0][0].fields[0];
    expect(newField.sort).toBe("asc");
    expect(newField.priority).toBe(0);
  });

  it("cycles asc → dsc", () => {
    const field = { pathStr: "name", sort: "asc", priority: 0, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [field] });
    query.toggleSort(field);
    expect(setQuery.mock.calls[0][0].fields[0].sort).toBe("dsc");
  });

  it("cycles dsc → null, clearing priority", () => {
    const field = { pathStr: "name", sort: "dsc", priority: 0, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [field] });
    query.toggleSort(field);
    const newField = setQuery.mock.calls[0][0].fields[0];
    expect(newField.sort).toBeNull();
    expect(newField.priority).toBeNull();
  });

  it("makes toggled field highest priority (0) and shifts others up", () => {
    const fieldA = { pathStr: "name", sort: "asc", priority: 0, pivoted: false };
    const fieldB = { pathStr: "book_count", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [fieldA, fieldB] });
    query.toggleSort(fieldB); // null → asc, becomes priority 0
    const fields = setQuery.mock.calls[0][0].fields;
    expect(fields[1].sort).toBe("asc");
    expect(fields[1].priority).toBe(0);
    expect(fields[0].priority).toBe(1); // was 0, bumped up
  });

  it("shifts lower priorities down when removing a sort", () => {
    const fieldA = { pathStr: "name", sort: "asc", priority: 0, pivoted: false };
    const fieldB = { pathStr: "book_count", sort: "dsc", priority: 1, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [fieldA, fieldB] });
    query.toggleSort(fieldA); // asc → dsc, making it priority 0; B shifts
    const fields = setQuery.mock.calls[0][0].fields;
    // After removing A's old sort: B.priority was 1 > 0 → B.priority = 0
    // Then setting new sort: both get +1, A gets priority 0
    expect(fields[0].sort).toBe("dsc");
    expect(fields[0].priority).toBe(0);
    expect(fields[1].priority).toBe(1);
  });
});

// ---- Query.togglePivot ----

describe("Query.togglePivot", () => {
  it("toggles pivot from false to true", () => {
    const field = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({ fields: [field] });
    query.togglePivot(field);
    expect(setQuery.mock.calls[0][0].fields[0].pivoted).toBe(true);
  });

  it("toggles pivot from true to false", () => {
    const field = { pathStr: "name", sort: null, priority: null, pivoted: true };
    const { query, setQuery } = makeQ({ fields: [field] });
    query.togglePivot(field);
    expect(setQuery.mock.calls[0][0].fields[0].pivoted).toBe(false);
  });
});

// ---- Query.addFilter ----

describe("Query.addFilter", () => {
  it("adds a filter using the type's defaultLookup and defaultValue", () => {
    const { query, setQuery } = makeQ();
    query.addFilter("name");
    expect(setQuery).toHaveBeenCalledWith({
      filters: [{ pathStr: "name", lookup: "equals", value: "" }],
    });
  });

  it("appends to existing filters", () => {
    const existing = { pathStr: "book_count", lookup: "equals", value: "0" };
    const { query, setQuery } = makeQ({ filters: [existing] });
    query.addFilter("name");
    const filters = setQuery.mock.calls[0][0].filters;
    expect(filters).toHaveLength(2);
    expect(filters[0]).toEqual(existing);
    expect(filters[1].pathStr).toBe("name");
  });
});

// ---- Query.filterForValue ----

describe("Query.filterForValue", () => {
  it("returns is_null filter for null value when is_null lookup exists", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", null, false)).toEqual({
      pathStr: "name",
      lookup: "is_null",
      value: "IsNull",
    });
  });

  it("returns is_null=NotNull for null value when negated", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", null, true)).toEqual({
      pathStr: "name",
      lookup: "is_null",
      value: "NotNull",
    });
  });

  it("returns equals filter for 'IsNull' string value (non-negated)", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", "IsNull", false)).toEqual({
      pathStr: "name",
      lookup: "equals",
      value: "IsNull",
    });
  });

  it("flips IsNull to NotNull when negated", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", "IsNull", true)).toEqual({
      pathStr: "name",
      lookup: "equals",
      value: "NotNull",
    });
  });

  it("flips NotNull to IsNull when negated", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", "NotNull", true)).toEqual({
      pathStr: "name",
      lookup: "equals",
      value: "IsNull",
    });
  });

  it("returns equals filter for a regular string value", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", "Alice", false)).toEqual({
      pathStr: "name",
      lookup: "equals",
      value: "Alice",
    });
  });

  it("returns not_equals filter for a regular string value when negated", () => {
    const { query } = makeQ();
    expect(query.filterForValue("name", "Alice", true)).toEqual({
      pathStr: "name",
      lookup: "not_equals",
      value: "Alice",
    });
  });

  it("coerces numeric values to strings", () => {
    const { query } = makeQ();
    expect(query.filterForValue("book_count", 42, false)).toEqual({
      pathStr: "book_count",
      lookup: "equals",
      value: "42",
    });
  });
});

// ---- Query.addExactFilter / addExactExclude ----

describe("Query.addExactFilter and addExactExclude", () => {
  it("addExactFilter appends an equals filter", () => {
    const { query, setQuery } = makeQ();
    query.addExactFilter("name", "Alice");
    const filters = setQuery.mock.calls[0][0].filters;
    expect(filters).toHaveLength(1);
    expect(filters[0]).toMatchObject({ lookup: "equals", value: "Alice" });
  });

  it("addExactExclude appends a not_equals filter", () => {
    const { query, setQuery } = makeQ();
    query.addExactExclude("name", "Alice");
    const filters = setQuery.mock.calls[0][0].filters;
    expect(filters).toHaveLength(1);
    expect(filters[0]).toMatchObject({ lookup: "not_equals", value: "Alice" });
  });
});

// ---- Query.removeFilter ----

describe("Query.removeFilter", () => {
  it("removes the filter at the given index", () => {
    const filters = [
      { pathStr: "name", lookup: "equals", value: "Alice" },
      { pathStr: "book_count", lookup: "gt", value: "5" },
    ];
    const { query, setQuery } = makeQ({ filters });
    query.removeFilter(0);
    expect(setQuery.mock.calls[0][0].filters).toEqual([filters[1]]);
  });

  it("removes the last filter leaving an empty array", () => {
    const filters = [{ pathStr: "name", lookup: "equals", value: "Alice" }];
    const { query, setQuery } = makeQ({ filters });
    query.removeFilter(0);
    expect(setQuery.mock.calls[0][0].filters).toEqual([]);
  });
});

// ---- Query.setFilterValue ----

describe("Query.setFilterValue", () => {
  it("updates the value at the given index", () => {
    const filters = [{ pathStr: "name", lookup: "equals", value: "" }];
    const { query, setQuery } = makeQ({ filters });
    query.setFilterValue(0, "Alice");
    expect(setQuery.mock.calls[0][0].filters[0].value).toBe("Alice");
  });

  it("does not affect other filters", () => {
    const filters = [
      { pathStr: "name", lookup: "equals", value: "" },
      { pathStr: "book_count", lookup: "gt", value: "0" },
    ];
    const { query, setQuery } = makeQ({ filters });
    query.setFilterValue(0, "Alice");
    expect(setQuery.mock.calls[0][0].filters[1].value).toBe("0");
  });
});

// ---- Query.setFilterLookup ----

describe("Query.setFilterLookup", () => {
  it("changes the lookup without resetting value when the lookup type is the same", () => {
    const filters = [{ pathStr: "name", lookup: "equals", value: "Alice" }];
    const { query, setQuery } = makeQ({ filters });
    query.setFilterLookup(0, "not_equals"); // both type 'string'
    const newFilter = setQuery.mock.calls[0][0].filters[0];
    expect(newFilter.lookup).toBe("not_equals");
    expect(newFilter.value).toBe("Alice");
  });

  it("resets value when the new lookup has a different type", () => {
    const filters = [{ pathStr: "name", lookup: "equals", value: "Alice" }];
    const { query, setQuery } = makeQ({ filters });
    query.setFilterLookup(0, "is_null"); // string → boolean
    const newFilter = setQuery.mock.calls[0][0].filters[0];
    expect(newFilter.lookup).toBe("is_null");
    expect(newFilter.value).not.toBe("Alice");
  });
});

// ---- Query.setLimit ----

describe("Query.setLimit", () => {
  it("sets a valid positive limit", () => {
    const { query, setQuery } = makeQ();
    query.setLimit(500);
    expect(setQuery).toHaveBeenCalledWith({ limit: 500 });
  });

  it("accepts a string and converts to number", () => {
    const { query, setQuery } = makeQ();
    query.setLimit("250");
    expect(setQuery).toHaveBeenCalledWith({ limit: 250 });
  });

  it("clamps 0 to 1", () => {
    const { query, setQuery } = makeQ();
    query.setLimit(0);
    expect(setQuery).toHaveBeenCalledWith({ limit: 1 });
  });

  it("clamps negative values to 1", () => {
    const { query, setQuery } = makeQ();
    query.setLimit(-100);
    expect(setQuery).toHaveBeenCalledWith({ limit: 1 });
  });
});

// ---- Query.setModel ----

describe("Query.setModel", () => {
  it("switches to the new model with empty fields, default filters, and default limit", () => {
    const { query, setQuery } = makeQ({
      fields: [{ pathStr: "name", sort: null, priority: null, pivoted: false }],
      filters: [{ pathStr: "name", lookup: "equals", value: "x" }],
    });
    query.setModel("Book");
    const call = setQuery.mock.calls[0][0];
    expect(call.model).toBe("Book");
    expect(call.fields).toEqual([]);
    expect(call.filters).toEqual(config.allModelFields.Book.defaultFilters);
    expect(call.limit).toBe(config.defaultRowLimit);
  });

  it("resets result data to empty", () => {
    const { query, setQuery } = makeQ();
    query.setModel("Book");
    const call = setQuery.mock.calls[0][0];
    expect(call.rows).toEqual(empty.rows);
    expect(call.cols).toEqual(empty.cols);
    expect(call.body).toEqual(empty.body);
  });
});

// ---- Field classification methods ----

describe("Query field set methods", () => {
  const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
  const bookCountField = { pathStr: "book_count", sort: null, priority: null, pivoted: false };
  const pivotedName = { pathStr: "name", sort: null, priority: null, pivoted: true };
  const errorField = {
    pathStr: "bad",
    sort: null,
    priority: null,
    pivoted: false,
    errorMessage: "unknown field",
  };

  it("validFields excludes fields with errorMessage", () => {
    const { query } = makeQ({ fields: [nameField, errorField] });
    expect(query.validFields().map((f) => f.pathStr)).toEqual(["name"]);
  });

  it("invalidFields returns only fields with errorMessage", () => {
    const { query } = makeQ({ fields: [nameField, errorField] });
    expect(query.invalidFields().map((f) => f.pathStr)).toEqual(["bad"]);
  });

  it("colFields returns pivoted valid fields", () => {
    const { query } = makeQ({ fields: [pivotedName, bookCountField] });
    expect(query.colFields().map((f) => f.pathStr)).toEqual(["name"]);
  });

  it("rowFields returns canPivot non-pivoted valid fields", () => {
    const { query } = makeQ({ fields: [nameField, bookCountField] });
    // name: canPivot=true, book_count: canPivot=false
    expect(query.rowFields().map((f) => f.pathStr)).toEqual(["name"]);
  });

  it("bodyFields returns non-canPivot valid fields", () => {
    const { query } = makeQ({ fields: [nameField, bookCountField] });
    expect(query.bodyFields().map((f) => f.pathStr)).toEqual(["book_count"]);
  });
});

// ---- Query.drillDown ----

describe("Query.drillDown", () => {
  it("adds a filter when a row field has multiple unique values", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({
      fields: [nameField],
      rows: [{ name: "Alice" }, { name: "Bob" }],
    });
    query.drillDown({ name: "Alice" });
    const filters = setQuery.mock.calls[0][0].filters;
    expect(filters).toHaveLength(1);
    expect(filters[0]).toMatchObject({ pathStr: "name", lookup: "equals", value: "Alice" });
  });

  it("does not add a filter when all rows have the same value", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({
      fields: [nameField],
      rows: [{ name: "Alice" }, { name: "Alice" }],
    });
    query.drillDown({ name: "Alice" });
    expect(setQuery.mock.calls[0][0].filters).toHaveLength(0);
  });

  it("skips fields not present in values", () => {
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({
      fields: [nameField],
      rows: [{ name: "Alice" }, { name: "Bob" }],
    });
    query.drillDown({}); // name is absent from values
    expect(setQuery.mock.calls[0][0].filters).toHaveLength(0);
  });

  it("skips non-canPivot fields (aggregates)", () => {
    const bookCountField = { pathStr: "book_count", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({
      fields: [bookCountField],
      rows: [{ book_count: 1 }, { book_count: 2 }],
    });
    query.drillDown({ book_count: 1 });
    expect(setQuery.mock.calls[0][0].filters).toHaveLength(0);
  });

  it("appends to existing filters", () => {
    const existing = { pathStr: "book_count", lookup: "gt", value: "0" };
    const nameField = { pathStr: "name", sort: null, priority: null, pivoted: false };
    const { query, setQuery } = makeQ({
      fields: [nameField],
      filters: [existing],
      rows: [{ name: "Alice" }, { name: "Bob" }],
    });
    query.drillDown({ name: "Alice" });
    const filters = setQuery.mock.calls[0][0].filters;
    expect(filters).toHaveLength(2);
    expect(filters[0]).toEqual(existing);
  });
});

// ---- Query.verbosePathStr ----

describe("Query.verbosePathStr", () => {
  it("returns the verboseName for a single field", () => {
    const { query } = makeQ();
    expect(query.verbosePathStr("name")).toBe("name");
  });

  it("joins names with a toMany arrow for related paths", () => {
    const { query } = makeQ();
    // books is toMany=true → uses ⇶ (U+21F6)
    expect(query.verbosePathStr("books__title")).toBe("books \u21f6 title");
  });
});

// ---- Query.getFieldClass ----

describe("Query.getFieldClass", () => {
  it("RelatedField: field has no type", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: null, concrete: true, canPivot: true, model: "Book", real: true })
    ).toBe("RelatedField");
  });

  it("CalculatedField: has type but not concrete", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: "string", concrete: false, canPivot: true, model: null, real: true })
    ).toBe("CalculatedField");
  });

  it("AggregateField: concrete but not canPivot", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: "number", concrete: true, canPivot: false, model: null, real: true })
    ).toBe("AggregateField");
  });

  it("FunctionField: concrete, canPivot, but no model", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: "string", concrete: true, canPivot: true, model: null, real: true })
    ).toBe("FunctionField");
  });

  it("AnnotatedField: concrete, canPivot, has model, but not real", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: "string", concrete: true, canPivot: true, model: "Book", real: false })
    ).toBe("AnnotatedField");
  });

  it("RealField: concrete, canPivot, has model, real", () => {
    const { query } = makeQ();
    expect(
      query.getFieldClass({ type: "string", concrete: true, canPivot: true, model: "Book", real: true })
    ).toBe("RealField");
  });
});

// ---- Query.getUrlForMedia ----

describe("Query.getUrlForMedia", () => {
  it("returns a full URL using the config baseUrl", () => {
    const { query } = makeQ({
      fields: [{ pathStr: "name", sort: null, priority: null, pivoted: false }],
    });
    const url = query.getUrlForMedia("csv");
    expect(url).toMatch(/^http:\/\/localhost\/data-browser\/query\/Author\//);
    expect(url).toContain(".csv");
  });
});
