// Power Query M Formula for FactTargets
let
    SourcePath = "data/processed/FactTargets.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=8, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"TargetKey", Int64.Type},
        {"TargetDate", type date},
        {"DateKey", Int64.Type},
        {"YearMonth", type text},
        {"TerritoryKey", Int64.Type},
        {"SalespersonKey", Int64.Type},
        {"RevenueTarget", type number},
        {"ProfitTarget", type number}
    })
in
    ChangeTypes
