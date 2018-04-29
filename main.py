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

# print 'start remove_by_ranking'
# homophily.remove_by_ranking(homophily.size, 1, 0, 'blogs')
# print 'stop remove_by_ranking'


###### AMD ######

homophily = Homophily('datasets/amd_network_class.gml')

print 'start remove_random'
homophily.remove_random(homophily.size, 'E', 'C', 'AMD')
print 'stop remove_random'


# class_part = utils.read_from_file_path('figures/all/blogs/remove_random_part')
# global_homo = utils.read_from_file('blogs', 'remove_by_ranking_global_homophilies')

# utils.plot_all(class_part, global_homo, 'blogs', 'remove_by_ranking')

# global_homophilies = utils.read_from_file('blogs', 'remove_with_probability_global_homophilies')
# utils.plot_global_homophily(global_homophilies, 'blogs', 'remove_with_probability')