
# // tag::imports[]
from graphframes import *
from pyspark import SparkContext, SQLContext
# // end::imports[]

# // tag::sqlcontext[]
sqlContext = SQLContext(sc)
# // end::sqlcontext[]

# // tag::load-graph-frame[]
v = sqlContext.read.csv("data/social-nodes.csv", header=True)
e = sqlContext.read.csv("data/social-relationships.csv", header=True)
g = GraphFrame(v, e)
# // end::load-graph-frame[]

# // tag::pagerank[]
results = g.pageRank(resetProbability=0.15, maxIter=20)
results.vertices.sort("pagerank", ascending=False).show()
# // end::pagerank[]

# // tag::personalized-pagerank[]
me = "Doug"
results = g.pageRank(resetProbability=0.15, maxIter=20, sourceId=me)
people_to_follow = results.vertices.sort("pagerank", ascending=False)

already_follows = list(g.edges.filter(f"src = '{me}'").toPandas()["dst"])
people_to_exclude = already_follows + [me]

people_to_follow[~people_to_follow.id.isin(people_to_exclude)].show()
# // end::personalized-pagerank[]
