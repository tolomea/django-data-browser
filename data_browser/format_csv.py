def head_cell(field):
    return [" ".join(field.pretty_path)]


def data_cell(value, span=1):
    return [value] + [""] * (span - 1)


def v_table_head_row(fields):
    res = []
    for field in fields:
        res += head_cell(field)
    return res


def v_table_body_row(fields, row):
    res = []
    for field in fields:
        if row:
            res += data_cell(row[field.path_str])
        else:
            res += [""]
    return res


def h_table_row(field, data, span):
    res = head_cell(field)
    for col in data:
        res += data_cell(col[field.path_str], span)
    return res


def get_csv_rows(bound_query, results):
    col_fields = bound_query.col_fields
    top_title_space = len(bound_query.row_fields) - 1
    side_title_space = (
        1 - len(bound_query.row_fields) if len(bound_query.col_fields) else 0
    )
    has_body = bound_query.row_fields or bound_query.body_fields

    # col headers and data aka pivots
    for field in col_fields:
        yield [""] * top_title_space + h_table_row(
            field=field, data=results["cols"], span=len(bound_query.body_fields)
        )

    if has_body:
        # body/aggregate headers
        row = [""] * side_title_space
        row += v_table_head_row(bound_query.row_fields)
        for _ in results["cols"] or [None]:
            row += v_table_head_row(bound_query.body_fields)
        yield row

        # row headers and body
        for row_index, row_data in enumerate(results["rows"]):
            row = [""] * side_title_space
            row += v_table_body_row(bound_query.row_fields, row_data)
            for table in results["body"]:
                row += v_table_body_row(bound_query.body_fields, table[row_index])
            yield row
