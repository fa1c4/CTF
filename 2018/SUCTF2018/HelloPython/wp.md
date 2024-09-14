# HelloPython

the output encrypted text: `f1f5d29b6e4414ec`

```shell
uncompyle6 attachment.pyc > attach.disa
```

uncompyle code
```python
(lambda __operator, __print, __g, __contextlib, __y: [(lambda __mod: [[[(lambda __items, __after, __sentinel: __y((lambda __this: (lambda : (lambda __i: [(lambda __out: (lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0]((lambda : __this()))][2])(__contextlib.nested(type('except', (), {'__enter__': (lambda self: None), '__exit__': (lambda __self, __exctype, __value, __traceback: __exctype is not None and [True for __out[0] in [(sys.exit(0), (lambda after: after()))[1]]][0])})(), type('try', (), {'__enter__': (lambda self: None), '__exit__': (lambda __self, __exctype, __value, __traceback: [False for __out[0] in [(v.append(int(word, 16)), (lambda __after: __after()))[1]]][0])})())))([None]) for __g['word'] in [__i]][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))))())(iter(p_text.split('_')), (lambda : [[[[[[[(lambda __after: __y((lambda __this: (lambda : (lambda __target: [(lambda __target: [(lambda __target: [[__this() for __g['n'] in [__operator.isub(__g['n'], 1)]][0] for __target.value in [__operator.iadd(__target.value, (y.value << 4) + k[2] ^ y.value + x.value ^ (y.value >> 5) + k[3])]][0])(z) for __target.value in [__operator.iadd(__target.value, (z.value << 4) + k[0] ^ z.value + x.value ^ (z.value >> 5) + k[1])]][0])(y) for __target.value in [__operator.iadd(__target.value, u)]][0])(x) if n > 0 else __after())))())((lambda : [[(__print(('').join(map(hex, w)).replace('0x', '').replace('L', '')), None)[1] for w[1] in [z.value]][0] for w[0] in [y.value]][0])) for __g['w'] in [[0, 0]]][0] for __g['n'] in [32]][0] for __g['u'] in [2654435769]][0] for __g['x'] in [c_uint32(0)]][0] for __g['z'] in [c_uint32(v[1])]][0] for __g['y'] in [c_uint32(v[0])]][0] for __g['k'] in [[3735928559, 590558003, 19088743, 4275878552]]][0]), []) for __g['v'] in [[]]][0] for __g['p_text'] in [raw_input('plain text:\n> ')]][0] for __g['c_uint32'] in [__mod.c_uint32]][0])(__import__('ctypes', __g, __g, ('c_uint32', ), 0)) for __g['sys'] in [__import__('sys', __g, __g)]][0])(__import__('operator', level=0), __import__('__builtin__', level=0).__dict__['print'], globals(), __import__('contextlib', level=0), (lambda f: (lambda x: x(x))((lambda y: f((lambda : y(y)()))))))
```

de-obfuscating the code above:
```python
(lambda __operator, __print, __g, __contextlib, __y:  # __operator=operator, __print=print, __g=globals(), __y用于构造循环
    [
        (lambda __mod: [
            [
                [
                    (lambda __items, __after, __sentinel: # __items=iter(p_text.split('_')), __after为加密函数, __sentinel=[]
                        __y(lambda __this: lambda: (lambda __i: [ # __i为当前循环到的__items
                            (
                                lambda __out: (
                                    lambda __ctx: [__ctx.__enter__(), __ctx.__exit__(None, None, None), __out[0](lambda: __this())][2]
                                )(
                                    __contextlib.nested(
                                        type(
                                            # 失败则退出程序
                                            'except', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: __exctype is not None and ([True for __out[0] in [((sys.exit(0), lambda after: after())[1])]][0])}
                                        )(), 
                                        type(
                                            # 尝试将 word以16进制转换为整形 存入 v
                                            'try', (), {'__enter__': lambda self: None, '__exit__': lambda __self, __exctype, __value, __traceback: [False for __out[0] in [((v.append(int(word, 16)), (lambda __after: __after()))[1])]][0]}
                                        )()
                                        )
                                )
                                # word = __i
                            )([None]) for __g['word'] in [(__i)]
                            # 循环__items
                        ][0] if __i is not __sentinel else __after())(next(__items, __sentinel)))()
                    )
                    (
                        # __items=iter(p_text.split('_'))
                        iter(p_text.split('_')), lambda: [
                            [
                                [
                                    [
                                        [
                                            [
                                                [
                                                    (
                                                        lambda __after: __y( # __after为后面参数中输出结果的lambda
                                                            lambda __this: lambda: ( # if n > 0 执行这部分代码，否则执行__after
                                                                lambda __target: [
                                                                    (
                                                                        lambda __target: [
                                                                            (
                                                                                lambda __target: [
                                                                                    # 循环调用__this()，效果等同于 while n > 0
                                                                                    # n -= 1
                                                                                    # z.value += ( y.value << 4 ) + k[2] ^ y.value + x.value ^ ( y.value >> 5 ) + k[3]
                                                                                    [__this() for __g['n'] in [(__operator.isub(__g['n'], 1))]][0] for __target.value in [(__operator.iadd(__target.value, ((((y.value << 4) + k[2]) ^ (y.value + x.value)) ^ ((y.value >> 5) + k[3]))))]
                                                                                ][0]
                                                                                # __target.value += ( z.value << 4 ) + k[0] ^ z.value + x.value ^ ( z.value >> 5 ) + k[1]
                                                                            )(z) for __target.value in [(__operator.iadd(__target.value, ((((z.value << 4) + k[0]) ^ (z.value + x.value)) ^ ((z.value >> 5) + k[1]))))]
                                                                        ][0]
                                                                        # __target.value += u
                                                                    )(y) for __target.value in [(__operator.iadd(__target.value, u))]
                                                                ][0]
                                                            )(x) if (n > 0) else __after() # 见上文
                                                        )()
                                                    )(
                                                        # 将z.value和y.value分别赋值给w[0]和w[1], 然后输出结果
                                                        lambda: [[(__print(''.join(map(hex, w)).replace('0x', '').replace('L', '')), None)[1] for w[1] in [(z.value)]][0] for w[0] in [(y.value)]][0]
                                                    ) for __g['w'] in [([0, 0])]  # w = [0,0]
                                                ][0] for __g['n'] in [(32)]  # n = 32
                                            ][0] for __g['u'] in [(2654435769)]  # u = 0x9e3779b9
                                        ][0] for __g['x'] in [(c_uint32(0))]  # x = c_uint32(0)
                                    ][0] for __g['z'] in [(c_uint32(v[1]))]  # z = c_uint32(v[1])
                                ][0] for __g['y'] in [(c_uint32(v[0]))]  # y = c_uint32(v[0])
                            ][0] for __g['k'] in [([3735928559, 590558003, 19088743, 4275878552])]  # k = [0xdeadbeef, 0x23333333, 0x01234567, 0xfedcba98]
                        ][0], []
                    ) for __g['v'] in [([])]  # v = []
                ][0] for __g['p_text'] in [(raw_input('plain text:\n> '))]  # p_text = raw_input("plain text:\n> ")
            ][0] for __g['c_uint32'] in [(__mod.c_uint32)]  # c_uint32 = ctypes.c_uint32
        ][0])
        (__import__('ctypes', __g, __g, ('c_uint32',), 0)) for __g['sys'] in [(__import__('sys', __g, __g))] # from ctypes import c_uint32    import sys
    ][0]
)
(__import__('operator', level=0), __import__('__builtin__', level=0).__dict__['print'], globals(), __import__('contextlib', level=0), (lambda f: (lambda x: x(x))(lambda y: f(lambda: y(y)()))))
```
TEA encryption algorithm
