from homophily import Homophily
import utils

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



# homo_list_before = read_from_file('add_random_homo_list_before')
# homo_list_after = read_from_file('add_random_homo_list_after')
# plot(homo_list_before, homo_list_after, 'add_random_homo_with_density')
global_homophilies = utils.read_from_file('AMD', 'add_random_global_homophilies')
utils.plot_global_homophily(global_homophilies, 'AMD', 'add_random')

