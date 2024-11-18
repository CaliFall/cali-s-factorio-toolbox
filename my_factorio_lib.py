import base64
import json
import zlib
import pyperclip

from pprint import pprint

from my_factorio_consts import DirectionType, ALL_SIGNAL_DICT, ALL_QUALITY_LIST

'''
异星工厂蓝图格式：
'blueprint' -> dict
				L 'entities' -> [dict]
				|               L 'direction'-> int
				|				L 'entity_number' -> int
				|				L 'name' -> str
				|				L 'position' -> dict
				|					            L 'x' -> float
				|					            L 'y' -> float
				L 'icons' -> [dict]
				|			    L 'index' -> int
				|			    L 'signal' -> dict
				|				    L 'name' -> str
				|				    L 'type' -> str
				L 'item': 'blueprint'
				L 'label' -> str (蓝图的名称)
				L 'description' -> str (蓝图的简介)
				L 'version' -> int (不清楚是什么)

带信号的常量运算器实体格式:
'control_behavior'
	L 'sections' -> dict
					L 'sections' -> [dict]
										L 'filters' -> [dict]
										|                L 'comparator': '='
										|                L 'count' -> int
										|                L 'index' -> int
										|                L 'name' -> str
										|                L 'quality' -> str('normal', 'uncommon', 'rare', 'epic', 'legendary')
										|                L 'type' -> str
										L 'index' -> int
'entity_number' -> int
'name': 'constant-combinator'
'position' -> dict
				L 'x' -> float
				L 'y' -> float

'''


def dict_to_blueprint(blueprint_dict: dict) -> str:
	"""将字典加密为蓝图"""
	
	try:
		json_data = json.dumps(blueprint_dict)  # 将蓝图数据转换为 JSON 字符串
		compressed_data = zlib.compress(json_data.encode('utf-8'))  # 压缩 JSON 数据
		base64_data = base64.b64encode(compressed_data).decode('utf-8')  # 编码为 Base64
		blueprint_string = f"0{base64_data}"  # 添加蓝图前缀
		return blueprint_string
	except Exception as e:
		raise e


def blueprint_to_dict(blueprint_string: str) -> dict:
	"""将蓝图代码解码为字典"""
	
	try:
		blueprint_string = blueprint_string[1:] if blueprint_string.startswith("0") else blueprint_string  # 去掉0前缀
		compressed_data = base64.b64decode(blueprint_string)  # Base64 解码
		json_data = zlib.decompress(compressed_data).decode('utf-8')  # 解压缩数据
		blueprint_data = json.loads(json_data)  # 反序列化为 JSON
		return blueprint_data
	except Exception as e:
		raise e


class Entity:
	"""实体对象"""
	
	def __init__(self, entity: dict | None = None) -> None:
		if entity is None:
			entity = {}
		
		self.entity_number = entity.get('entity_number')  # 实体序号
		self.name = entity.get('name')  # 名称
		self.type = entity.get('type')  # 类型
		self.position_x = entity.get('position', {}).get('x', 0)  # 位置x
		self.position_y = entity.get('position', {}).get('y', 0)  # 位置y
		self.direction = entity.get('direction')  # 朝向
		
		# 非共有
		self.control_behavior = None
	
	def get_dict(self) -> dict:
		"""获得该实体对象的字典格式"""
		_ = {'position': {'x': self.position_x, 'y': self.position_y}}
		
		if self.entity_number:
			_['entity_number'] = self.entity_number
		if self.name:
			_['name'] = self.name
		if self.type:
			_['type'] = self.type
		if self.direction:
			_['direction'] = self.direction
		if self.control_behavior:
			_['control_behavior'] = self.control_behavior
		
		return _
	
	def replace(self, name: str = None, type: str = None) -> None:
		"""用新的name或type来置换当前实体"""
		if name:
			self.name = name
		if type:
			self.type = type
	
	def rotate_to(self, direction: int) -> None:
		"""旋转实体"""
		self.direction = direction


class ConstantCombinator(Entity):
	"""常量运算器"""
	
	def __init__(self, entity: dict | None = None) -> None:
		if entity is None:
			entity = {}
		super().__init__(entity)
		
		self.name = 'constant-combinator'
		
		# 控制行为
		self.control_behavior = entity.get('control_behavior')
		if not self.control_behavior:
			self.init_control_behavior()
		
		self.filter_count = 0  # 总过滤器数量
	
	def init_control_behavior(self) -> None:
		"""初始化行为"""
		self.control_behavior = {'sections': {'sections': []}}
	
	def set_filter(
			self, section_index: int = 1, filter_index: int = 1,
			name: str = '', type: str = '', count: int = 1,
			quality: str = 'normal') -> None:
		"""手动设置过滤器"""
		has_section = False
		for sec in self.control_behavior['sections']['sections']:
			if sec['index'] == section_index:
				has_section = True
				break
		if not has_section:
			self.control_behavior['sections']['sections'].append({'filters': [], 'index': section_index})
		
		for sec in self.control_behavior['sections']['sections']:
			if sec['index'] == section_index:
				sec['filters'].append({
					'comparator': '=',
					'count': count,
					'index': filter_index,
					'name': name,
					'type': type,
					'quality': quality
				})
	
	def add_filter_auto(self, count: int = 1) -> None:
		"""
		自动根据序号添加过滤器
		主要用于显示屏存储大量数据
		"""
		
		this_filter_global_index = self.filter_count
		this_filter_local_index = this_filter_global_index % 1000 + 1
		this_filter_section_index = this_filter_global_index // 1000 + 1
		
		if len(self.control_behavior['sections']['sections']) < this_filter_section_index:
			self.control_behavior['sections']['sections'].append({'filters': [], 'index': this_filter_section_index})
		
		signal = {
			'comparator': '=',
			'count': count,
			'index': this_filter_local_index,
			'name': ALL_SIGNAL_DICT[str(this_filter_global_index // 5)]['name'],
			'quality': ALL_QUALITY_LIST[this_filter_global_index % 5]
		}
		
		if 'type' in ALL_SIGNAL_DICT[str(this_filter_global_index // 5)]:
			signal['type'] = ALL_SIGNAL_DICT[str(this_filter_global_index // 5)]['type']
		
		self.control_behavior['sections']['sections'][this_filter_section_index - 1]['filters'].append(signal)
		
		self.filter_count += 1


class DeciderCombinator(Entity):
	"""判断运算器"""
	
	def __init__(self, entity: dict | None = None) -> None:
		if entity is None:
			entity = {}
		super().__init__(entity)
		
		self.name = 'decider-combinator'
		
		# 控制行为
		self.control_behavior = entity.get('control_behavior')
		if not self.control_behavior:
			self.init_control_behavior()
	
	def init_control_behavior(self) -> None:
		"""初始化行为"""
		self.control_behavior = {'decider_conditions': {
			'conditions': [],
			'outputs': []
		}}
		
		self.conditions = self.control_behavior['decider_conditions']['conditions']
		self.outputs = self.control_behavior['decider_conditions']['outputs']
	
	def add_condition(
			self, comparator: str = "<", constant: int = 0,
			first_signal_name: str = '', first_signal_type: str = '',
			first_use_red_network: bool = True, first_use_green_network: bool = True,
			second_signal_name: str = '', second_signal_type: str = '',
			second_use_red_network: bool = True, second_use_green_network: bool = True) -> None:
		"""添加条件"""
		_ = {
			'first_signal_networks': {'red': first_use_red_network, 'green': first_use_green_network},
			'second_signal_networks': {'red': second_use_red_network, 'green': second_use_green_network}
		}
		if comparator:
			_['comparator'] = comparator
		if constant:
			_['constant'] = constant
		if first_signal_name:
			_['first_signal'] = {'name': first_signal_name}
			if first_signal_type:
				_['first_signal']['type'] = first_signal_type
		if second_signal_name:
			_['second_signal'] = {'name': second_signal_name}
			if second_signal_type:
				_['second_signal']['type'] = second_signal_type
		self.conditions.append(_)
	
	def add_output(
			self, signal_name: str = '', signal_type: str = '',
			copy_count_from_input: bool = True,
			use_red_network: bool = True,
			use_green_network: bool = True) -> None:
		"""添加输出"""
		_ = {
			'copy_count_from_input': copy_count_from_input,
			'networks': {
				'green': use_green_network,
				'red': use_red_network}}
		if signal_name:
			_['signal'] = {'name': signal_name}
			if signal_type:
				_['signal']['type'] = signal_type
		self.outputs.append(_)


class ArithmeticCombinator(Entity):
	"""算术运算器"""
	
	def __init__(self, entity: dict | None = None) -> None:
		if entity is None:
			entity = {}
		super().__init__(entity)
		
		self.name = 'arithmetic-combinator'
		
		# 控制行为
		self.control_behavior = entity.get('control_behavior')
		if not self.control_behavior:
			self.init_control_behavior()
	
	def init_control_behavior(self):
		"""初始化行为"""
		self.control_behavior = {'arithmetic_conditions': {}}
	
	def set_first_signal(self, name: str = '', type: str = ''):
		"""设置第一信号"""
		self.control_behavior['arithmetic_conditions']['first_signal'] = {'name': name, 'type': type}
	
	def set_second_signal(self, name: str = '', type: str = ''):
		"""设置第二信号"""
		self.control_behavior['arithmetic_conditions']['second_signal'] = {'name': name, 'type': type}
	
	def set_output_signal(self, name: str = '', type: str = ''):
		"""设置输出信号"""
		self.control_behavior['arithmetic_conditions']['output_signal'] = {'name': name, 'type': type}
	
	def set_operation(self, operation: str = '*'):
		"""设置运算符"""
		self.control_behavior['arithmetic_conditions']['operation'] = operation
	
	def set_first_constant(self, constant=0):
		"""设置第一常量"""
		self.control_behavior['arithmetic_conditions']['first_constant'] = constant
	
	def set_second_constant(self, constant=0):
		"""设置第二常量"""
		self.control_behavior['arithmetic_conditions']['second_constant'] = constant


class Icon:
	"""图标对象"""
	
	def __init__(self, icon: dict) -> None:
		self.index = icon.get('index')
		self.signal = {
			'name': icon.get('signal').get('name'),
			'type': icon.get('signal').get('type'),
		}
	
	def get_dict(self) -> dict:
		_ = {'index': self.index, 'signal': {}}
		if self.signal['name']:
			_['signal']['name'] = self.signal['name']
		if self.signal['type']:
			_['signal']['type'] = self.signal['type']
		return _


class Blueprint:
	"""蓝图对象"""
	
	def __init__(self, blueprint_dict: dict | None = None) -> None:
		if blueprint_dict is None:
			blueprint_dict = {}
		
		blueprint = blueprint_dict.get('blueprint', {})
		
		self.label = blueprint.get('label')  # 名称
		self.description = blueprint.get('description')  # 简介
		self.version = blueprint.get('version')  # 版本号
		self.wires = blueprint.get('wires')  # 线缆数据
		self.icons = [Icon(x) for x in blueprint.get('icons', [])]  # 图标列表
		self.entities = [Entity(x) for x in blueprint.get('entities', [])]  # 实体列表
	
	def get_dict(self) -> dict:
		"""获得该蓝图对象的字典形式"""
		_ = {'item': 'blueprint'}
		
		if self.label:
			_['label'] = self.label
		if self.description:
			_['description'] = self.description
		if self.version:
			_['version'] = self.version
		if self.wires:
			_['wires'] = self.wires
		if self.icons:
			_['icons'] = [x.get_dict() for x in self.icons]
		if self.entities:
			_['entities'] = [x.get_dict() for x in self.entities]
		
		return {'blueprint': _}
	
	def get_entities_number(self) -> int:
		"""获取实体总数"""
		return len(self.entities)
	
	def add_entity(self, entity: Entity, entity_number: int = 0) -> None:
		"""添加实体"""
		if not entity_number:
			entity.entity_number = len(self.entities) + 1
		
		self.entities.append(entity)
	
	def connect_entity(
			self, first_entity: Entity, second_entity: Entity,
			connect_code: str = 'ii', wire_type: str = '') -> None:
		"""将实体用信号线连接在一起"""
		if not first_entity.entity_number or not second_entity.entity_number:
			raise KeyError
		
		if not self.wires:
			self.wires = []
		
		match connect_code:
			case 'ii':
				if 'r' in wire_type:
					self.wires.append([first_entity.entity_number, 1, second_entity.entity_number, 1])
				if 'g' in wire_type:
					self.wires.append([first_entity.entity_number, 2, second_entity.entity_number, 2])
			case 'io':
				if 'r' in wire_type:
					self.wires.append([first_entity.entity_number, 1, second_entity.entity_number, 3])
				if 'g' in wire_type:
					self.wires.append([first_entity.entity_number, 2, second_entity.entity_number, 4])
			case 'oi':
				if 'r' in wire_type:
					self.wires.append([first_entity.entity_number, 3, second_entity.entity_number, 1])
				if 'g' in wire_type:
					self.wires.append([first_entity.entity_number, 4, second_entity.entity_number, 2])
			case 'oo':
				if 'r' in wire_type:
					self.wires.append([first_entity.entity_number, 3, second_entity.entity_number, 3])
				if 'g' in wire_type:
					self.wires.append([first_entity.entity_number, 4, second_entity.entity_number, 4])
			case _:
				raise KeyError


if __name__ == '__main__':
	with open('blueprint_cache.txt', 'r', encoding='utf-8') as f:
		bp = f.read()
	
	bp_dict = blueprint_to_dict(bp)
	pprint(bp_dict)
	
	bp_object = Blueprint(bp_dict)  # 对象化
	
	for entity in bp_object.entities:
		entity.rotate_to(DirectionType.SOUTH_EAST.value)
	
	pyperclip.copy(dict_to_blueprint(bp_object.get_dict()))
