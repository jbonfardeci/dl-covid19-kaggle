create procedure dbo.usp_UpdatePaperKeyworRanks as

truncate table dbo.PaperKeywordRankByQuestion;

insert into dbo.PaperKeywordRankByQuestion(paper_id)
    select paper_id from dbo.AllPapers;

update dbo.PaperKeywordRankByQuestion set q01 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 1
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q02 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 2
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q03 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 3
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q04 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 4
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q05 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 5
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q06 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 6
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q07 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 7
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q08 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 8
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q09 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 9
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;

update dbo.PaperKeywordRankByQuestion set q10 = q.KeywordRank
from (
    select paper_id , (KeywordCount - min(KeywordCount) over()) / (max(KeywordCount) over() - min(KeywordCount) over()) as KeywordRank
    from dbo.vw_KeywordRankByQuestion where QuestionNum = 10
) as q
where dbo.PaperKeywordRankByQuestion.paper_id = q.paper_id;