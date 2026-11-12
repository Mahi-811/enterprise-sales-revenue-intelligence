// Power Query M Formula for DimTerritory
let
    SourcePath = "data/processed/DimTerritory.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=4, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"TerritoryKey", Int64.Type},
        {"TerritoryName", type text},
        {"Region", type text},
        {"Country", type text}
    })
in
    ChangeTypes
