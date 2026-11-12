// Power Query M Formula for DimCustomer
let
    SourcePath = "data/processed/DimCustomer.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=9, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"CustomerKey", Int64.Type},
        {"CustomerID", type text},
        {"CustomerName", type text},
        {"Segment", type text},
        {"City", type text},
        {"State", type text},
        {"Country", type text},
        {"Region", type text},
        {"AcquisitionDate", type date}
    })
in
    ChangeTypes
