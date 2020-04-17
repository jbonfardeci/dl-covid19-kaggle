

$outputDir = "C:\Users\bonfardeci-j\source\dl-covid19-kaggle-contest\Data\{0}";

$conf = @{
    server = "10.24.1.181";
    dbname = "covid19";
    username = ""; 
    pwd = "";
    is_trusted_conn = $false;
    delimiter = ",";
    dllPath = "C:\mahso\bin\EasyCsvLib.dll";
}

# Load EasyCsv library
[System.Reflection.Assembly]::LoadFrom($conf.dllPath);

$connectionString = "Data Source=" + $conf.server + "; Initial Catalog=" + $conf.dbname + ";";

if($conf.is_trusted_conn) {
    $connectionString += "Trusted_Connection=True;";
} else {
    $connectionString += "User Id="+ $conf.username +"; Password=" + $conf.pwd + "; Trusted_Connection=False; Encrypt=False;"
}

function exportCsv($path, $connectionString, $queryString){
    $success = $false;
    $writer = New-Object EasyCsvLib.CsvWriter($path, $connectionString, $queryString);
    $success = $writer.OutputToCsv();
    $writer.Dispose();

    return $success;
}

#$tables = @("dbo.AllPapers", "dbo.Author", "dbo.JournalMapping", "dbo.Institution", "dbo.Authored", "dbo.PublishedBy", "dbo.Citation", "dbo.Affiliation")
$tables = @("dbo.vw_TableauTable");

foreach($table in $tables){
    $path = [string]::Format($outputDir, "$table.csv");
    $queryString = "SELECT * FROM $table";
    $success = exportCsv $path $connectionString $queryString;
    echo "Export $table $success";
}