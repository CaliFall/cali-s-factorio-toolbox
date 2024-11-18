from PIL import Image, ImageEnhance, ImageFile

from my_factorio_lib import *

"""测试用函数"""


def generate_all_signal_dict():
	# 用于生成全物品名称枚举
	
	# bp = '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'
	bp = '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'
	bp_dict = blueprint_to_dict(bp)
	
	filter_list = bp_dict['blueprint']['entities'][0]['control_behavior']['sections']['sections'][0]['filters']
	filter_list.sort(key=lambda x: x['name'])
	
	all_item_dict = {}
	
	for i in range(len(filter_list)):
		all_item_dict[str(i)] = {}
		all_item_dict[str(i)]['name'] = filter_list[i]['name']
		if 'type' in filter_list[i]:
			all_item_dict[str(i)]['type'] = filter_list[i]['type']
	
	print(str(all_item_dict).replace('}, ', '},\n'))


def generate_all_item_constant_combinator_blueprint() -> str:
	# 生成一个包含全信号的常量运算器蓝图
	
	item_dict_list = []
	
	for i in range(len(ALL_SIGNAL_DICT)):
		_ = {
			'comparator': '=',
			'count': 1,
			'index': i + 1,
			'name': ALL_SIGNAL_DICT[str(i)]['name'],
			'quality': 'normal'
		}
		
		if 'type' in ALL_SIGNAL_DICT[str(i)]:
			_['type'] = ALL_SIGNAL_DICT[str(i)]['type']
		
		item_dict_list.append(_)
	
	d = {'blueprint': {'entities': [{'control_behavior': {'sections': {'sections': [
		{
			'filters': item_dict_list,
			'index': 1
		}
	]}},
		'entity_number': 1,
		'name': 'constant-combinator',
		'position': {'x': 0, 'y': 0}}],
		'icons': [
			{
				'index': 1,
				'signal': {'name': 'constant-combinator'}
			}],
		'item': 'blueprint'}}
	
	return dict_to_blueprint(d)


def generate_one_item_constant_combinator_blueprint() -> str:
	# 生成单个常量运算器蓝图
	#
	# 用于单独测试某个name是否可以作为信号
	
	item_dict_list = []
	
	_ = {
		'comparator': '=',
		'count': 1,
		'index': 1,
		'name': 'wooden-chest-explosion',
		'quality': 'uncommon',
		'type': 'explosion'
	}
	
	item_dict_list.append(_)
	
	d = {'blueprint': {'entities': [{'control_behavior': {'sections': {'sections': [
		{
			'filters': item_dict_list,
			'index': 1
		}
	]}},
		'entity_number': 1,
		'name': 'constant-combinator',
		'position': {'x': 0, 'y': 0}}],
		'icons': [
			{
				'index': 1,
				'signal': {'name': 'constant-combinator'}
			}],
		'item': 'blueprint'}}
	
	return dict_to_blueprint(d)


"""生产用函数"""


def generate_screen_blueprint(
		width: int = 10, height: int = 10,
		wire_type_list: list | None = None,
		always_on: bool = True) -> str:
	"""参数化生成彩色显示屏"""
	
	if width * height > 2985:
		print('像素总和超过2985上限！')
		return ''
	
	d = {
		'blueprint': {
			'entities': [],
			'item': 'blueprint',
			'wires': [],
		}
	}
	
	for x in range(width):
		for y in range(height):
			_ = {
				'entity_number': y * width + x + 1,
				'name': 'small-lamp',
				'position': {'x': x, 'y': y},
				'control_behavior': {
					'color_mode': 2,
					'use_colors': True,
					'rgb_signal': {},
				},
				'always_on': always_on
			}
			
			_['control_behavior']['rgb_signal']['name'] = ALL_SIGNAL_DICT[str((y * width + x) // 5)]['name']
			_['control_behavior']['rgb_signal']['quality'] = ALL_QUALITY_LIST[(y * width + x) % 5]
			
			if 'type' in ALL_SIGNAL_DICT[str((y * width + x) // 5)]:
				_['control_behavior']['rgb_signal']['type'] = ALL_SIGNAL_DICT[str((y * width + x) // 5)]['type']
			
			d['blueprint']['entities'].append(_)
	
	if wire_type_list:
		for x in range(width):
			for y in range(height):
				if (x + 1) % width == 0 and y > 0:  # 连接最后一列电灯
					if 1 in wire_type_list:
						d['blueprint']['wires'].append([(y - 1) * width + x + 1, 1, y * width + x + 1, 1])
					if 2 in wire_type_list:
						d['blueprint']['wires'].append([(y - 1) * width + x + 1, 2, y * width + x + 1, 2])
				
				if x > 0:  # 连接水平电灯
					if 1 in wire_type_list:
						d['blueprint']['wires'].append([y * width + x, 1, y * width + x + 1, 1])
					if 2 in wire_type_list:
						d['blueprint']['wires'].append([y * width + x, 2, y * width + x + 1, 2])
	
	return dict_to_blueprint(d)


def get_gif_duration(gif_path: str) -> int:
	"""获取一个gif的帧间间隔，单位为tick"""
	
	gif = Image.open(gif_path)
	duration_ms = int(gif.info['duration'])
	duration_tick = int(duration_ms * 0.06)
	return duration_tick


def get_frame_rgb_list(frame: ImageFile, width: int = 10, height: int = 10) -> list:
	"""获取一个图片的像素rgb列表"""
	
	frame = frame.resize((width, height))
	
	enhancer = ImageEnhance.Contrast(frame)
	frame = enhancer.enhance(1.5)
	
	pix = frame.load()
	
	width = frame.size[0]
	height = frame.size[1]
	
	_ = []
	
	for x in range(width):
		for y in range(height):
			rgb = pix[y, x]
			if not len(rgb) == 3:
				rgb = rgb[:-1]
			_.append(rgb)
	
	return _


def generate_mini_static_image_blueprint(img_path: str, width: int = 10, height: int = 10) -> str:
	"""参数化生成小静态图片蓝图"""
	
	bp_object = Blueprint()
	cc_object = ConstantCombinator()
	
	rgb_list = get_frame_rgb_list(Image.open(img_path), width, height)
	for i in range(len(rgb_list)):
		cc_object.add_filter_auto(count=rgb_list[i][0] << 16 | rgb_list[i][1] << 8 | rgb_list[i][2])
	
	bp_object.add_entity(cc_object)
	return dict_to_blueprint(bp_object.get_dict())


def generate_mini_dynamic_image_blueprint(gif_path: str, width: int = 10, height: int = 10, duration: int = 1) -> str:
	"""参数化生成小动态图片蓝图"""
	
	gif = Image.open(gif_path)
	print("n_frames={}".format(gif.n_frames))
	print("duration={}ms".format(gif.info['duration']))
	
	bp_object = Blueprint()
	
	# 生成常量运算器
	image_cc_list = []  # 存储每一帧图形的常量运算器列表
	for i in range(gif.n_frames):
		gif.seek(i)
		rgb_list = get_frame_rgb_list(gif.convert('RGB'), width, height)
		
		cc_object = ConstantCombinator()
		bp_object.add_entity(cc_object)
		image_cc_list.append(cc_object)
		
		cc_object.position_x = 0.5
		cc_object.position_y = i + 0.5
		cc_object.rotate_to(DirectionType.EAST.value)
		
		for p in range(len(rgb_list)):
			cc_object.add_filter_auto(count=rgb_list[p][0] << 16 | rgb_list[p][1] << 8 | rgb_list[p][2])
	
	# 生成与常量运算器配对的判断运算器
	image_select_dc_list = []
	for i in range(gif.n_frames):
		dc_object = DeciderCombinator()
		bp_object.add_entity(dc_object)
		image_select_dc_list.append(dc_object)
		
		dc_object.position_x = 2
		dc_object.position_y = i + 0.5
		dc_object.rotate_to(DirectionType.EAST.value)
		dc_object.add_condition(
			comparator='=', constant=i,
			first_signal_name='signal-dot', first_signal_type='virtual', first_use_red_network=False
		)
		dc_object.add_output(signal_name='signal-everything', signal_type='virtual', use_green_network=False)
		
		if i == gif.n_frames - 1:
			dc_object.add_condition(
				comparator='=', constant=i + 1,
				first_signal_name='signal-dot', first_signal_type='virtual',
				first_use_red_network=False, first_use_green_network=True,
			)
	
	# 连接图片存储器和选择器的红线
	for i in range(len(image_cc_list)):
		bp_object.connect_entity(image_cc_list[i], image_select_dc_list[i], 'ii', 'r')
	
	# 将所有选择器用红绿线相连
	for i in range(len(image_select_dc_list)):
		if i == 0:
			continue
		bp_object.connect_entity(image_select_dc_list[i - 1], image_select_dc_list[i], 'ii', 'g')
		bp_object.connect_entity(image_select_dc_list[i - 1], image_select_dc_list[i], 'oo', 'rg')
	
	# 生成控制模块中的常量运算器
	control_cc_object = ConstantCombinator()
	bp_object.add_entity(control_cc_object)
	control_cc_object.position_x = 0.5
	control_cc_object.position_y = -2.5
	control_cc_object.rotate_to(DirectionType.SOUTH.value)
	control_cc_object.set_filter(1, 1, 'signal-dot', 'virtual', 1)
	
	# 生成控制模块中的判断运算器
	control_dc_object = DeciderCombinator()
	bp_object.add_entity(control_dc_object)
	control_dc_object.position_x = 0.5
	control_dc_object.position_y = -1.0
	control_dc_object.rotate_to(DirectionType.SOUTH.value)
	control_dc_object.add_condition(
		comparator="<", constant=gif.n_frames * duration, first_signal_name='signal-dot',
		first_signal_type='virtual')
	control_dc_object.add_output(signal_name='signal-everything', signal_type='virtual')
	
	# 生成控制模块中的算术运算器
	control_ac_object = ArithmeticCombinator()
	bp_object.add_entity(control_ac_object)
	control_ac_object.position_x = 1.5
	control_ac_object.position_y = -1.0
	control_ac_object.rotate_to(DirectionType.SOUTH.value)
	control_ac_object.set_first_signal('signal-dot', 'virtual')
	control_ac_object.set_operation("/")
	control_ac_object.set_second_constant(duration)
	control_ac_object.set_output_signal('signal-dot', 'virtual')
	
	# 连接控制模块信号线
	bp_object.connect_entity(control_cc_object, control_dc_object, 'ii', 'r')
	bp_object.connect_entity(control_dc_object, control_dc_object, 'io', 'r')
	bp_object.connect_entity(control_dc_object, control_ac_object, 'ii', 'r')
	bp_object.connect_entity(control_ac_object, image_select_dc_list[0], 'oi', 'g')
	
	return dict_to_blueprint(bp_object.get_dict())


if __name__ == '__main__':
	from pprint import pprint
	import pyperclip
	
	# with open('blueprint_cache.txt', 'r') as f:
	# 	bp = f.read()
	#
	# bp = blueprint_to_dict(bp)
	# pprint(bp)
	
	# for e in bp['blueprint']['entities']:
	# 	e['quality'] = QualityType.LEGENDARY.value
	# pyperclip.copy(dict_to_blueprint(bp))
	
	# pyperclip.copy(generate_one_item_constant_combinator_blueprint())
	
	# pyperclip.copy(generate_screen_blueprint(53, 53, wire_type_list=[2]))
	# pyperclip.copy(generate_image_blueprint('cali.png', 10, 10))
	
	pyperclip.copy(
		generate_mini_dynamic_image_blueprint(
			'D:/Github/Projects/cali-s-factorio-blueprints/toolbox/media/earth.gif', 54, 54))
	
	pass
