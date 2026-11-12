// Power Query M Formula for UserSecurityMapping
let
    SourcePath = "data/processed/UserSecurityMapping.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=3, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"UserEmail", type text},
        {"TerritoryKey", Int64.Type},
        {"Role", type text}
    })
in
    ChangeTypes
