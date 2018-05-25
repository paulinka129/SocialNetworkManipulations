from homophily import Homophily
import utils
import consts

### badania ###

# edges = utils.read_edge_list()
# nodes = utils.read_node_list()
# utils.write_gml_file(nodes, edges)

# homophily = Homophily('datasets/amd_network_class.gml')


# homophily2 = Homophily('datasets/polblogs.gml')
# homophily3 = Homophily('datasets/polblogs.gml')

# print nx.info(homophily.G)
# print '################'
# homophily.remove_random_nodes(100)
# homophily.pick_with_probability(20)
# print 'koniec'
# print nx.info(homophily.G)
# homophily.plot_homophily(homophily.local_homophily(), 'local.png')
# homophily.plot_homophily(homophily.global_homophily(), 'global.png')
# homophily.global_homophily()
# homophily.add_by_ranking(1,1)

# print 'start add_random'
# homophily.add_random(homophily.size, 'E', 'AMD')
# print 'stop add_random'

# print 'start add_with_probability'
# homophily2.add_with_probability(homophily2.size, Consts.class1)
# print 'stop add_with_probability'

# print 'start add_by_ranking'
# homophily3.add_by_ranking(homophily3.size, Consts.class1)
# print 'stop add_by_ranking'

# print 'start remove_random'
# homophily.remove_random(homophily.size, Consts.class0)
# print 'stop remove_random'

# print 'start remove_with_probability'
# homophily2.remove_with_probability(homophily.size, Consts.class0)
# print 'stop remove_with_probability'

# print 'start remove_by_ranking'
# homophily3.remove_by_ranking(homophily.size, Consts.class0)
# print 'stop remove_by_ranking'

# global_homophilies = homophily3.read_from_file('add_random_global_homophilies')
# homophily3.plot_global(global_homophilies, 'add_random')
# print '#########'



# homo_list_before = utils.read_from_file('blogs','remove_with_probability_homo_list_before')
# homo_list_after = utils.read_from_file('blogs', 'remove_with_probability_homo_list_after')
# utils.plot_local_homophily(homo_list_before, homo_list_after, 'blogs', 'remove_with_probability')
# global_homophilies = utils.read_from_file('blogs', 'remove_with_probability_global_homophilies')
# utils.plot_global_homophily(global_homophilies, 'blogs', 'remove_with_probability')






###### BLOGS ######

# homophily = Homophily('datasets/polblogs.gml')

# print 'start remove_random'
# homophily.remove_random(homophily.size, 1, 0, 'blogs')
# print 'stop remove_random'

# print 'start remove_with_probability'
# homophily.remove_with_probability(homophily.size, 1, 0, 'blogs')
# print 'stop remove_with_probability'

# print('start remove_bychange_class_by_ranking_ranking')
# homophily.change_class_by_ranking(homophily.size, 1, 0, 'blogs')
# print('stop change_class_by_ranking')


###### AMD ######

# homophily = Homophily('datasets/amd_network_class.gml')

# print 'start remove_random'
# homophily.remove_random(homophily.size, 'E', 'C', 'AMD')
# print 'stop remove_random'

# print 'start change_class_random'
# homophily.change_class_by_ranking(homophily.size, 'E', 'C', 'AMD')
# print 'stop change_class_random'

# pp1,p1 = homophily.pick_nodes_with_probability(20)
# pp2,p2 = homophily.pick_nodes_with_probability(20)
# pp3,p3 = homophily.pick_nodes_with_probability(20)
# print pp1
# print pp2
# print pp3


# class_part = utils.read_from_file_path('figures/all/blogs/remove_random_part')
# global_homo = utils.read_from_file('blogs', 'remove_by_ranking_global_homophilies')

# utils.plot_all(class_part, global_homo, 'blogs', 'remove_by_ranking')

# global_homophilies = utils.read_from_file('AMD', 'remove_random_global_homophilies')
# utils.plot_global_homophily(global_homophilies, 'AMD', 'remove_random')


# homophily = Homophily('datasets/amd_network_class.gml')

# print(homophily.clas_list)

# homophily.manipulate(homophily.remove_strategy, 'remove_with_probability', homophily.pick_with_probability, 'E', 'AMD')
# # homophily.remove_random(homophily.size, 'E', 'E', 'AMD')
# print(homophily.homophily_per_clas)

# homophily = Homophily('datasets/polblogs.gml')
# homophily.manipulate(homophily.remove_strategy, 'remove_with_probability', homophily.pick_with_probability, 1, 'blogs')

# homophily = Homophily('datasets/amd_network_class.gml')
# homophily.manipulate(homophily.remove_strategy, 'remove_by_ranking', homophily.pick_by_ranking, 'E', 'AMD')

# homophily = Homophily('datasets/amd_network_class.gml')
# homophily.manipulate(homophily.change_class_strategy, 'change_class_random', homophily.pick_random, 'E', 'AMD')

# homophily = Homophily('datasets/amd_network_class.gml')
# print('start')
# homophily.evaluate_lbp_with_add_manipulation('E')
# print('end')

### change_class_by_ranking ###

# class_partition = utils.read_from_file('blogs', 'change_class_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'change_class_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'change_class_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'change_class_by_ranking')

# class_partition = utils.read_from_file('AMD', 'change_class_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'change_class_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'change_class_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'change_class_by_ranking')

# class_partition = utils.read_from_file('CSphd', 'change_class_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'change_class_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'change_class_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'change_class_by_ranking')

# class_partition = utils.read_from_file('Yeast', 'change_class_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'change_class_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'change_class_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'change_class_by_ranking')


### change_class_by_pagerank ### 

# class_partition = utils.read_from_file('blogs', 'change_class_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'change_class_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'change_class_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'change_class_by_pagerank')

# class_partition = utils.read_from_file('AMD', 'change_class_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'change_class_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'change_class_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'change_class_by_pagerank')

# class_partition = utils.read_from_file('CSphd', 'change_class_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'change_class_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'change_class_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'change_class_by_pagerank')

# class_partition = utils.read_from_file('Yeast', 'change_class_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'change_class_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'change_class_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'change_class_by_pagerank')


### change_class_random

# class_partition = utils.read_from_file('blogs', 'change_class_random_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'change_class_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'change_class_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'change_class_random')

# class_partition = utils.read_from_file('AMD', 'change_class_random_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'change_class_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'change_class_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'change_class_random')

# class_partition = utils.read_from_file('CSphd', 'change_class_random_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'change_class_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'change_class_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'change_class_random')

# class_partition = utils.read_from_file('Yeast', 'change_class_random_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'change_class_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'change_class_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'change_class_random')


### change_class_with_probability

# class_partition = utils.read_from_file('blogs', 'change_class_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'change_class_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'change_class_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'change_class_with_probability')

# class_partition = utils.read_from_file('AMD', 'change_class_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'change_class_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'change_class_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'change_class_with_probability')

# class_partition = utils.read_from_file('CSphd', 'change_class_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'change_class_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'change_class_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'change_class_with_probability')

# class_partition = utils.read_from_file('Yeast', 'change_class_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'change_class_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'change_class_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'change_class_with_probability')


### remove_by_pagerank

# class_partition = utils.read_from_file('blogs', 'remove_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'remove_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'remove_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'remove_by_pagerank')

# class_partition = utils.read_from_file('AMD', 'remove_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'remove_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'remove_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'remove_by_pagerank')

# class_partition = utils.read_from_file('CSphd', 'remove_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'remove_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'remove_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'remove_by_pagerank')

# class_partition = utils.read_from_file('Yeast', 'remove_by_pagerank_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'remove_by_pagerank_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'remove_by_pagerank_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'remove_by_pagerank')

### remove_by_ranking

# class_partition = utils.read_from_file('blogs', 'remove_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'remove_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'remove_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'remove_by_ranking')

# class_partition = utils.read_from_file('AMD', 'remove_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'remove_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'remove_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'remove_by_ranking')

# class_partition = utils.read_from_file('CSphd', 'remove_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'remove_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'remove_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'remove_by_ranking')

# class_partition = utils.read_from_file('Yeast', 'remove_by_ranking_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'remove_by_ranking_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'remove_by_ranking_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'remove_by_ranking')

### remove_random

# class_partition = utils.read_from_file('blogs', 'remove_random_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'remove_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'remove_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'remove_random')

# class_partition = utils.read_from_file('AMD', 'remove_random_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'remove_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'remove_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'remove_random')

# class_partition = utils.read_from_file('CSphd', 'remove_random_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'remove_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'remove_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'remove_random')

# class_partition = utils.read_from_file('Yeast', 'remove_random_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'remove_random_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'remove_random_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'remove_random')

### remove_with_probability

# class_partition = utils.read_from_file('blogs', 'remove_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('blogs', 'remove_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('blogs', 'remove_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'remove_with_probability')

# class_partition = utils.read_from_file('AMD', 'remove_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('AMD', 'remove_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('AMD', 'remove_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'remove_with_probability')

# class_partition = utils.read_from_file('CSphd', 'remove_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('CSphd', 'remove_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('CSphd', 'remove_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'remove_with_probability')

# class_partition = utils.read_from_file('Yeast', 'remove_with_probability_class_partitions')
# homophily_per_clas = utils.read_json('Yeast', 'remove_with_probability_homophily_per_clas.json')
# global_homophilies = utils.read_from_file('Yeast', 'remove_with_probability_global_homophilies')
# utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'remove_with_probability')

### add_big_random

class_partition = utils.read_from_file('blogs', 'add_big_random_class_partitions')
homophily_per_clas = utils.read_json('blogs', 'add_big_random_homophily_per_clas.json')
global_homophilies = utils.read_from_file('blogs', 'add_big_random_global_homophilies')
utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '1', 'blogs', 'add_big_random')

class_partition = utils.read_from_file('AMD', 'add_big_random_class_partitions')
homophily_per_clas = utils.read_json('AMD', 'add_big_random_homophily_per_clas.json')
global_homophilies = utils.read_from_file('AMD', 'add_big_random_global_homophilies')
utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'E', 'AMD', 'add_big_random')

class_partition = utils.read_from_file('CSphd', 'add_big_random_class_partitions')
homophily_per_clas = utils.read_json('CSphd', 'add_big_random_homophily_per_clas.json')
global_homophilies = utils.read_from_file('CSphd', 'add_big_random_global_homophilies')
utils.plot_all(class_partition, global_homophilies, homophily_per_clas, '80', 'CSphd', 'add_big_random')

class_partition = utils.read_from_file('Yeast', 'add_big_random_class_partitions')
homophily_per_clas = utils.read_json('Yeast', 'add_big_random_homophily_per_clas.json')
global_homophilies = utils.read_from_file('Yeast', 'add_big_random_global_homophilies')
utils.plot_all(class_partition, global_homophilies, homophily_per_clas, 'U', 'Yeast', 'add_big_random')