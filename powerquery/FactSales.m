// Power Query M Formula for FactSales
let
    // Configure FilePath parameter or default relative path
    SourcePath = "data/processed/FactSales.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=12, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"OrderLineID", Int64.Type},
        {"OrderID", type text},
        {"OrderDate", type date},
        {"DateKey", Int64.Type},
        {"CustomerKey", Int64.Type},
        {"ProductKey", Int64.Type},
        {"SalespersonKey", Int64.Type},
        {"TerritoryKey", Int64.Type},
        {"Quantity", Int64.Type},
        {"UnitPrice", type number},
        {"DiscountAmount", type number},
        {"UnitCost", type number}
    }),
    FilteredNonZeroQuantity = Table.SelectRows(ChangeTypes, each [Quantity] > 0)
in
    FilteredNonZeroQuantity
