[System.Reflection.Assembly]::LoadFrom("C:\mahso\bin\EasyCsvLib.dll");

$outputDir = "C:\Users\bonfardeci-j\Desktop\covid-19\csv\{0}";
$connectionString = "Server=zbook27\mssqlserver17;Database=covid19;Trusted_Connection=yes;";

function exportCsv($path, $connectionString, $queryString){
    $success = $false;
    $writer = New-Object EasyCsvLib.CsvWriter($path, $connectionString, $queryString);
    $success = $writer.OutputToCsv();
    $writer.Dispose();

    return $success;
}

$tables = @("dbo.AllPapers", "dbo.Author", "dbo.JournalMapping", "dbo.Institution", "dbo.Authored", "dbo.PublishedBy", "dbo.Citation", "dbo.Affiliation")

foreach($table in $tables){
    $path = [string]::Format($outputDir, "$table.csv");
    $queryString = "SELECT * FROM $table";
    $success = exportCsv $path $connectionString $queryString;
    echo "Export $table $success";
}