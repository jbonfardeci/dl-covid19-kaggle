# change the $vars to your setup.

$conf = @{
    tableName = "AllSourcesMetadata";
    sql = $null;
    source = "../Data/all_sources_metadata_2020-03-13_clean.csv";
    server = ".\mssqlserver17";
    dbname = "covid19";
    username = $null; 
    pwd = $null;
    is_trusted_conn = $true;
    delimiter = ",";
    truncate = $false;
    dllPath = "../bin/EasyCsvLib.dll";
}

# Load EasyCsv library
[System.Reflection.Assembly]::LoadFrom($conf.dllPath);

$connectionString = "Data Source=" + $conf.server + "; Initial Catalog=" + $conf.dbname + ";";

if($conf.is_trusted_conn) {
    $connectionString += "Trusted_Connection=True;";
} else {
    $connectionString += "User Id="+ $conf.username +"; Password=" + $conf.pwd + "; Trusted_Connection=False; Encrypt=False;"
}

function execute_sql($query){
    $cmd = New-Object system.data.sqlclient.SqlCommand;
    $cmd.Connection = New-Object system.data.sqlclient.SqlConnection;
    $cmd.Connection.ConnectionString = $connectionString;
    $cmd.CommandTimeout = 300;
    $cmd.CommandText = $query;
    $cmd.Connection.Open();
    $res = $cmd.ExecuteNonQuery();
    $cmd.Connection.Close();
    $cmd.Dispose();
}

# Import CSV file
function importCsv($path, $tableName, $delimiter, $headerRowCount = 1, $colNames = $null, $batchSize = 1000, $timeOut = 1500){
    $csv = Test-Path $path -ErrorAction Stop
    $success = $false;

    $reader = New-Object EasyCsvLib.CsvReader($path, $tableName, $connectionString, $delimiter, $headerRowCount, $colNames, $batchSize, $timeOut);
    $reader.Verbose = $true;

    Write-Host "Importing...";
    $reader.ImportCsv();
    $rowsAdded = $reader.RowsWritten;
    $totalRows = $reader.TotalDataRows;
    $batchCount = $reader.BatchCount;

    if($rowsAdded -ge $totalRows) {
       $success = $true;
       Write-Host "Success! All $totalRows rows were imported to the database.";
    }
    else {
       Write-Error "Error! Only $rowsAdded of $totalRows rows were imported to the database.";
    }

    $reader.Dispose();

    return $success;
}

$src = $conf.source;
$tbl = $conf.tableName;

if($conf.sql -ne $null){
    write-host "Creating table $tbl...";
    $sql = Get-Content -Raw -LiteralPath $conf.sql;
    execute_sql $sql;
    write-host "Table $tbl created.";
}

if($conf.truncate){
    write-host "Truncating $tbl...";
    execute_sql "truncate table $tbl";
    write-host "Truncated $tbl.";
}

Write-Host "Writing $fileName to $tbl";

importCsv $src $tbl $conf.delimiter;
