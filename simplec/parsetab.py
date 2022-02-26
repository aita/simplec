
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'rightEQUALleftEQUAL_EQUALNOT_EQUALleftLESSGREATERLESS_EQUALGREATER_EQUALleftPLUSMINUSleftTIMESDIVIDEDIVIDE ELSE EQUAL EQUAL_EQUAL GREATER GREATER_EQUAL IF LBRACE LESS LESS_EQUAL LPAREN MINUS NAME NOT_EQUAL NUMBER PLUS RBRACE RETURN RPAREN SEMICOLON TIMES\n        program : statement_list\n        \n        statement_list :\n        \n        statement_list : statement\n        \n        statement_list : statement_list statement\n        \n        statement : expression SEMICOLON\n                  | return\n                  | if\n                  | compound\n        \n        compound : LBRACE statement_list RBRACE\n        \n        if : IF LPAREN expression RPAREN statement\n        \n        if : IF LPAREN expression RPAREN statement ELSE statement\n        \n        return : RETURN expression SEMICOLON\n               | RETURN SEMICOLON\n        \n        expression : binary\n                | unary\n                | primary\n                | assign\n        \n        assign : expression EQUAL expression\n        \n        binary : expression PLUS expression\n            | expression MINUS expression\n            | expression TIMES expression\n            | expression DIVIDE expression\n            | expression EQUAL_EQUAL expression\n            | expression NOT_EQUAL expression\n            | expression LESS expression\n            | expression GREATER expression\n            | expression LESS_EQUAL expression\n            | expression GREATER_EQUAL expression\n        \n        unary : PLUS expression\n            | MINUS expression\n        \n        primary : NUMBER\n        \n        primary : NAME\n        \n        primary : LPAREN expression RPAREN\n        '
    
_lr_action_items = {'RETURN':([0,2,3,5,6,7,15,20,21,34,37,51,54,55,56,57,58,],[12,12,-3,-6,-7,-8,12,-4,-5,-13,12,-12,-9,12,-10,12,-11,]),'IF':([0,2,3,5,6,7,15,20,21,34,37,51,54,55,56,57,58,],[13,13,-3,-6,-7,-8,13,-4,-5,-13,13,-12,-9,13,-10,13,-11,]),'LBRACE':([0,2,3,5,6,7,15,20,21,34,37,51,54,55,56,57,58,],[15,15,-3,-6,-7,-8,15,-4,-5,-13,15,-12,-9,15,-10,15,-11,]),'PLUS':([0,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[16,16,-3,22,-6,-7,-8,-14,-15,-16,-17,16,16,16,16,16,-31,-32,-4,-5,16,16,16,16,16,16,16,16,16,16,16,22,-13,16,22,16,-29,-30,-19,-20,-21,-22,22,22,22,22,22,22,22,-12,22,-33,-9,16,-10,16,-11,]),'MINUS':([0,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[17,17,-3,23,-6,-7,-8,-14,-15,-16,-17,17,17,17,17,17,-31,-32,-4,-5,17,17,17,17,17,17,17,17,17,17,17,23,-13,17,23,17,-29,-30,-19,-20,-21,-22,23,23,23,23,23,23,23,-12,23,-33,-9,17,-10,17,-11,]),'NUMBER':([0,2,3,5,6,7,12,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,51,54,55,56,57,58,],[18,18,-3,-6,-7,-8,18,18,18,18,18,-4,-5,18,18,18,18,18,18,18,18,18,18,18,-13,18,18,-12,-9,18,-10,18,-11,]),'NAME':([0,2,3,5,6,7,12,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,51,54,55,56,57,58,],[19,19,-3,-6,-7,-8,19,19,19,19,19,-4,-5,19,19,19,19,19,19,19,19,19,19,19,-13,19,19,-12,-9,19,-10,19,-11,]),'LPAREN':([0,2,3,5,6,7,12,13,14,15,16,17,20,21,22,23,24,25,26,27,28,29,30,31,32,34,35,37,51,54,55,56,57,58,],[14,14,-3,-6,-7,-8,14,35,14,14,14,14,-4,-5,14,14,14,14,14,14,14,14,14,14,14,-13,14,14,-12,-9,14,-10,14,-11,]),'$end':([0,1,2,3,5,6,7,20,21,34,51,54,56,58,],[-2,0,-1,-3,-6,-7,-8,-4,-5,-13,-12,-9,-10,-11,]),'RBRACE':([3,5,6,7,15,20,21,34,37,51,54,56,58,],[-3,-6,-7,-8,-2,-4,-5,-13,54,-12,-9,-10,-11,]),'SEMICOLON':([4,8,9,10,11,12,18,19,33,38,39,40,41,42,43,44,45,46,47,48,49,50,53,],[21,-14,-15,-16,-17,34,-31,-32,51,-29,-30,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-18,-33,]),'TIMES':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[24,-14,-15,-16,-17,-31,-32,24,24,24,24,24,24,-21,-22,24,24,24,24,24,24,24,24,-33,]),'DIVIDE':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[25,-14,-15,-16,-17,-31,-32,25,25,25,25,25,25,-21,-22,25,25,25,25,25,25,25,25,-33,]),'EQUAL_EQUAL':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[26,-14,-15,-16,-17,-31,-32,26,26,-29,-30,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,26,26,-33,]),'NOT_EQUAL':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[27,-14,-15,-16,-17,-31,-32,27,27,-29,-30,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,27,27,-33,]),'LESS':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[28,-14,-15,-16,-17,-31,-32,28,28,-29,-30,-19,-20,-21,-22,28,28,-25,-26,-27,-28,28,28,-33,]),'GREATER':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[29,-14,-15,-16,-17,-31,-32,29,29,-29,-30,-19,-20,-21,-22,29,29,-25,-26,-27,-28,29,29,-33,]),'LESS_EQUAL':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[30,-14,-15,-16,-17,-31,-32,30,30,-29,-30,-19,-20,-21,-22,30,30,-25,-26,-27,-28,30,30,-33,]),'GREATER_EQUAL':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[31,-14,-15,-16,-17,-31,-32,31,31,-29,-30,-19,-20,-21,-22,31,31,-25,-26,-27,-28,31,31,-33,]),'EQUAL':([4,8,9,10,11,18,19,33,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[32,-14,-15,-16,-17,-31,-32,32,32,-29,-30,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,32,32,-33,]),'ELSE':([5,6,7,21,34,51,54,56,58,],[-6,-7,-8,-5,-13,-12,-9,57,-11,]),'RPAREN':([8,9,10,11,18,19,36,38,39,40,41,42,43,44,45,46,47,48,49,50,52,53,],[-14,-15,-16,-17,-31,-32,53,-29,-30,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,-18,55,-33,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,15,],[2,37,]),'statement':([0,2,15,37,55,57,],[3,20,3,20,56,58,]),'expression':([0,2,12,14,15,16,17,22,23,24,25,26,27,28,29,30,31,32,35,37,55,57,],[4,4,33,36,4,38,39,40,41,42,43,44,45,46,47,48,49,50,52,4,4,4,]),'return':([0,2,15,37,55,57,],[5,5,5,5,5,5,]),'if':([0,2,15,37,55,57,],[6,6,6,6,6,6,]),'compound':([0,2,15,37,55,57,],[7,7,7,7,7,7,]),'binary':([0,2,12,14,15,16,17,22,23,24,25,26,27,28,29,30,31,32,35,37,55,57,],[8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,8,]),'unary':([0,2,12,14,15,16,17,22,23,24,25,26,27,28,29,30,31,32,35,37,55,57,],[9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,9,]),'primary':([0,2,12,14,15,16,17,22,23,24,25,26,27,28,29,30,31,32,35,37,55,57,],[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,]),'assign':([0,2,12,14,15,16,17,22,23,24,25,26,27,28,29,30,31,32,35,37,55,57,],[11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,11,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',121),
  ('statement_list -> <empty>','statement_list',0,'p_statement_list_null','parser.py',127),
  ('statement_list -> statement','statement_list',1,'p_statement_list_first','parser.py',133),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list_rest','parser.py',139),
  ('statement -> expression SEMICOLON','statement',2,'p_statement','parser.py',145),
  ('statement -> return','statement',1,'p_statement','parser.py',146),
  ('statement -> if','statement',1,'p_statement','parser.py',147),
  ('statement -> compound','statement',1,'p_statement','parser.py',148),
  ('compound -> LBRACE statement_list RBRACE','compound',3,'p_compound_statement','parser.py',154),
  ('if -> IF LPAREN expression RPAREN statement','if',5,'p_if','parser.py',160),
  ('if -> IF LPAREN expression RPAREN statement ELSE statement','if',7,'p_if_else','parser.py',166),
  ('return -> RETURN expression SEMICOLON','return',3,'p_return','parser.py',172),
  ('return -> RETURN SEMICOLON','return',2,'p_return','parser.py',173),
  ('expression -> binary','expression',1,'p_expression','parser.py',182),
  ('expression -> unary','expression',1,'p_expression','parser.py',183),
  ('expression -> primary','expression',1,'p_expression','parser.py',184),
  ('expression -> assign','expression',1,'p_expression','parser.py',185),
  ('assign -> expression EQUAL expression','assign',3,'p_assign','parser.py',191),
  ('binary -> expression PLUS expression','binary',3,'p_binary','parser.py',198),
  ('binary -> expression MINUS expression','binary',3,'p_binary','parser.py',199),
  ('binary -> expression TIMES expression','binary',3,'p_binary','parser.py',200),
  ('binary -> expression DIVIDE expression','binary',3,'p_binary','parser.py',201),
  ('binary -> expression EQUAL_EQUAL expression','binary',3,'p_binary','parser.py',202),
  ('binary -> expression NOT_EQUAL expression','binary',3,'p_binary','parser.py',203),
  ('binary -> expression LESS expression','binary',3,'p_binary','parser.py',204),
  ('binary -> expression GREATER expression','binary',3,'p_binary','parser.py',205),
  ('binary -> expression LESS_EQUAL expression','binary',3,'p_binary','parser.py',206),
  ('binary -> expression GREATER_EQUAL expression','binary',3,'p_binary','parser.py',207),
  ('unary -> PLUS expression','unary',2,'p_unary','parser.py',213),
  ('unary -> MINUS expression','unary',2,'p_unary','parser.py',214),
  ('primary -> NUMBER','primary',1,'p_primary_number','parser.py',220),
  ('primary -> NAME','primary',1,'p_primary_name','parser.py',226),
  ('primary -> LPAREN expression RPAREN','primary',3,'p_primary_paren','parser.py',241),
]
