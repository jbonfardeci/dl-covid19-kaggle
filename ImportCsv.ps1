<#
    Options:  
    -dir : directory read CSV data sets from
    -del : Delimiter. Default = ","
    -s : The full database server address
    -c : database name
    -tbl : table name
    -q : SQL file to create table
    -src : data source filename
    -u : SQL auth database username
    -p : SQL auth database password
    -t : if using trusted database connection. Default = FALSE
    -help
#>
# change the $vars to your setup.

$conf = @{
    tableName = "AllSourcesMetadata";
    sql = "C:\Users\bonfardeci-j\source\repos\dl\covid19_kaggle\Tables\all_sources_metadata.sql";
    source = "C:\Users\bonfardeci-j\source\repos\dl\covid19_kaggle\Data\all_sources_metadata_2020-03-13_clean.csv";
    server = "zbook27\mssqlserver17";
    dbname = "covid19";
    username = $null; 
    pwd = $null;
    is_trusted_conn = $true;
    delimiter = ",";
    truncate = $false;
    dllPath = "C:\Users\bonfardeci-j\source\repos\dl\covid19_kaggle\bin\EasyCsvLib.dll";
}

# Load EasyCsv library
[System.Reflection.Assembly]::LoadFrom($conf.dllPath);

$break = $false;

# Parse command line arguments.
for($i=0; $i -lt $args.Length; $i++){
    $arg = $args[$i];
    $next_arg = $args[$i+1];

    switch($arg){
        "-help"{
            write-host "  
            -dir : directory read CSV data sets from
            -del : Delimiter. Default = ","
            -s : The full database server address
            -c : database name
            -tbl : table name
            -q : SQL file to create table
            -src : data source filename
            -u : SQL auth database username
            -p : SQL auth database password
            -t : if using trusted database connection. Default = FALSE
            -help";
            $break = $true;
        }
        "-dir"{
            $conf.dir = $next_arg;
        }
        "-del"{
            $conf.delimiter = $next_arg;
        }
        "-s" { 
            $conf.server = $next_arg; 
        }
        "-c" { 
            $conf.dbname = $next_arg; 
        }
        "-src" {
            $conf.source = $next_arg;
        }
        "-tbl" {
            $conf.tableName = $next_arg;
        }
        "-q" {
            $conf.sql = $next_arg;
        }
        "-u" { 
            $conf.username = $next_arg;
            $conf.is_trusted_conn = $false;
        }
        "-p" { 
            $conf.pwd = $next_arg;
            $conf.is_trusted_conn = $false;
        }
        "-t" { 
            $conf.is_trusted_conn = $true;
            if($conf.username.Length -gt 0 -or $conf.pwd.Length -gt 0){
                write-error "Warning: setting trusted connection will override SQL authentication with username and password.";
            }
        }
        "-truncate"{
            $conf.truncate = ($next_arg -match "true");
        }
    }
}

if($break){
    return;
}

if($conf.server.Length -eq 0){
    throw 'Error: The server name (-s) is required.';
}
elseif($conf.dbname.Length -eq 0){
    throw 'Error: The database name (-c) is required.';
}
elseif(-not $conf.is_trusted_conn -and ($conf.username.Length -eq 0 -or $conf.pwd.Length -eq 0) ){
	throw 'Error: SQL auth username (-u) and password (-p) are required if not using trusted connection (-t).';
}


$connectionString = "Data Source=" + $conf.server + "; Initial Catalog=" + $conf.dbname + ";";

if($conf.is_trusted_conn) {
    $connectionString += "Trusted_Connection=True;";
} else {
    $connectionString += "User Id="+ $conf.username +"; Password=" + $conf.pwd + "; Trusted_Connection=False; Encrypt=True;"
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
function importCsv($path, $tableName, $delimiter, $headerRowCount = 1, $colNames = $null, $batchSize = 50000, $timeOut = 1500){
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
