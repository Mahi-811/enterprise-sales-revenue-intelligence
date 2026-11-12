// Power Query M Formula for DimDate
let
    SourcePath = "data/processed/DimDate.csv",
    Source = Csv.Document(File.Contents(SourcePath), [Delimiter=",", Columns=13, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromoteHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    ChangeTypes = Table.TransformColumnTypes(PromoteHeaders, {
        {"DateKey", Int64.Type},
        {"Date", type date},
        {"Year", Int64.Type},
        {"Quarter", type text},
        {"YearQuarter", type text},
        {"Month", Int64.Type},
        {"MonthName", type text},
        {"MonthShort", type text},
        {"YearMonth", type text},
        {"Week", Int64.Type},
        {"DayOfWeek", Int64.Type},
        {"DayName", type text},
        {"IsWorkingDay", Int64.Type}
    })
in
    ChangeTypes
