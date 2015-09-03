from django.shortcuts import render
from django.http.response import JsonResponse
from elastic.search import ElasticQuery, Search
from elastic.query import Query, TermsFilter, Filter, FilteredQuery
from elastic.elastic_settings import ElasticSettings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import Http404
from django.contrib import messages


@ensure_csrf_cookie
def gene_page(request):
    ''' Renders a gene page. '''
    query_dict = request.GET
    gene = query_dict.get("g")
    if gene is None:
        messages.error(request, 'No gene name given.')
        raise Http404()
    query = ElasticQuery(Query.ids([gene]))
    elastic = Search(query, idx=ElasticSettings.idx('GENE'), size=5)
    res = elastic.search()
    if res.hits_total == 1:
        context = {'gene': res.docs[0], 'ens_id': gene}
        return render(request, 'gene/gene.html', context,
                      content_type='text/html')
    elif res.hits_total == 0:
        messages.error(request, 'Gene '+gene+' not found.')
        raise Http404()


def pub_details(request):
    ''' Get PMID details. '''
    pmids = request.POST.getlist("pmids[]")
    query = ElasticQuery(Query.ids(pmids))
    elastic = Search(query, idx=ElasticSettings.idx('PUBLICATION'), size=len(pmids))
    return JsonResponse(elastic.get_json_response()['hits'])


def interaction_details(request):
    ''' Get interaction details for a given ensembl ID. '''
    ens_id = request.POST.get('ens_id')
    query = ElasticQuery.has_parent('gene', Query.ids(ens_id))
    elastic = Search(query, idx=ElasticSettings.idx('GENE'), size=500)

    interaction_hits = elastic.get_json_response()['hits']
    ens_ids = []
    for hit in interaction_hits['hits']:
        for interactor in hit['_source']['interactors']:
            ens_ids.append(interactor['interactor'])
    docs = _get_gene_docs_by_ensembl_id(ens_ids, ['symbol'])
    for hit in interaction_hits['hits']:
        for interactor in hit['_source']['interactors']:
            iid = interactor['interactor']
            try:
                interactor['symbol'] = getattr(docs[iid], 'symbol')
            except KeyError:
                interactor['symbol'] = iid

    return JsonResponse(interaction_hits)


def genesets_details(request):
    ''' Get gene sets for a given ensembl ID. '''
    ens_id = request.POST.get('ens_id')
    geneset_filter = Filter(Query.query_string(ens_id, fields=["gene_sets"]).query_wrap())
    query = ElasticQuery.filtered(Query.match_all(), geneset_filter)
    elastic = Search(query, idx=ElasticSettings.idx('GENE'), size=500)
    genesets_hits = elastic.get_json_response()['hits']
    ens_ids = []
    for hit in genesets_hits['hits']:
        for ens_id in hit['_source']['gene_sets']:
            ens_ids.append(ens_id)
    docs = _get_gene_docs_by_ensembl_id(ens_ids, ['symbol'])

    for hit in genesets_hits['hits']:
        genesets = {}
        for ens_id in hit['_source']['gene_sets']:
            try:
                genesets[ens_id] = getattr(docs[ens_id], 'symbol')
            except KeyError:
                genesets[ens_id] = ens_id
        hit['_source']['gene_sets'] = genesets
    return JsonResponse(genesets_hits)


def _get_gene_docs_by_ensembl_id(ens_ids, sources=None):
    ''' Get the gene symbols for the corresponding array of ensembl IDs.
    A dictionary is returned with the key being the ensembl ID and the
    value the gene document. '''
    query = ElasticQuery(Query.ids(ens_ids), sources=sources)
    elastic = Search(query, idx=ElasticSettings.idx('GENE'), size=len(ens_ids))
    return {doc.doc_id(): doc for doc in elastic.search().docs}
