create procedure dbo.usp_UpdateJournalsFromIMport as

update dbo.JournalMapping set 
    StandardJournalName = i.StandardJournalName
    , ImpactFactor = i.ImpactFactor
    , PrintISSN = i.PrintISSN
    , ElectronicISSN = i.ElectronicISSN
    , Publisher = i.Publisher
    , ChiefEditor = i.ChiefEditor
from 
    import.journalsSUBMISSIONV3 as i
where 
    dbo.JournalMapping.JournalNameInData = i.JournalNameInData;