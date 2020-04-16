
CREATE procedure [dbo].[usp_UpdateKmeansClusters] as 
update dbo.AllPapers set KmeansCluster = k.cluster 
from import.paper_kmeans_clusters as k 
where dbo.AllPapers.paper_id = k.paper_id;