// Power Query M Formula for DimProduct
let
    SourcePath = "data/processed/DimProduct.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"ProductKey", Int64.Type},
        {"ProductID", type text},
        {"ProductName", type text},
        {"Category", type text},
        {"Subcategory", type text},
        {"Brand", type text},
        {"StandardCost", type number},
        {"ListPrice", type number}
    })
in
    ChangeTypes
