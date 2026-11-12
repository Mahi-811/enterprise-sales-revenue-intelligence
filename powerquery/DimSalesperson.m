// Power Query M Formula for DimSalesperson
let
    SourcePath = "data/processed/DimSalesperson.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"SalespersonKey", Int64.Type},
        {"SalespersonID", type text},
        {"SalespersonName", type text},
        {"Email", type text},
        {"Manager", type text},
        {"TerritoryKey", Int64.Type}
    })
in
    ChangeTypes
