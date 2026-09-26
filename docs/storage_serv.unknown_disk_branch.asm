
.\storage_serv:     file format elf64-x86-64


Disassembly of section .text:

0000000001207d00 <crosscall2@@Base+0xc5fbe0>:
 1207d00:	94                   	xchg   esp,eax
 1207d01:	24 a8                	and    al,0xa8
 1207d03:	04 00                	add    al,0x0
 1207d05:	00 0f                	add    BYTE PTR [rdi],cl
 1207d07:	10 42 08             	adc    BYTE PTR [rdx+0x8],al
 1207d0a:	0f 11 84 24 b0 04 00 	movups XMMWORD PTR [rsp+0x4b0],xmm0
 1207d11:	00 
 1207d12:	0f 10 42 18          	movups xmm0,XMMWORD PTR [rdx+0x18]
 1207d16:	0f 11 84 24 c0 04 00 	movups XMMWORD PTR [rsp+0x4c0],xmm0
 1207d1d:	00 
 1207d1e:	0f 10 42 28          	movups xmm0,XMMWORD PTR [rdx+0x28]
 1207d22:	0f 11 84 24 d0 04 00 	movups XMMWORD PTR [rsp+0x4d0],xmm0
 1207d29:	00 
 1207d2a:	0f 10 42 38          	movups xmm0,XMMWORD PTR [rdx+0x38]
 1207d2e:	0f 11 84 24 e0 04 00 	movups XMMWORD PTR [rsp+0x4e0],xmm0
 1207d35:	00 
 1207d36:	48 83 bc 24 c0 04 00 	cmp    QWORD PTR [rsp+0x4c0],0x7
 1207d3d:	00 07 
 1207d3f:	90                   	nop
 1207d40:	75 a9                	jne    1207ceb <crosscall2@@Base+0xc5fbcb>
 1207d42:	4c 8b 94 24 b8 04 00 	mov    r10,QWORD PTR [rsp+0x4b8]
 1207d49:	00 
 1207d4a:	41 81 3a 73 79 73 70 	cmp    DWORD PTR [r10],0x70737973
 1207d51:	75 98                	jne    1207ceb <crosscall2@@Base+0xc5fbcb>
 1207d53:	66 41 81 7a 04 61 74 	cmp    WORD PTR [r10+0x4],0x7461
 1207d5a:	75 8f                	jne    1207ceb <crosscall2@@Base+0xc5fbcb>
 1207d5c:	41 80 7a 06 68       	cmp    BYTE PTR [r10+0x6],0x68
 1207d61:	75 88                	jne    1207ceb <crosscall2@@Base+0xc5fbcb>
 1207d63:	4c 89 8c 24 d8 01 00 	mov    QWORD PTR [rsp+0x1d8],r9
 1207d6a:	00 
 1207d6b:	48 89 94 24 08 04 00 	mov    QWORD PTR [rsp+0x408],rdx
 1207d72:	00 
 1207d73:	48 8b 84 24 c8 04 00 	mov    rax,QWORD PTR [rsp+0x4c8]
 1207d7a:	00 
 1207d7b:	48 8b 9c 24 d0 04 00 	mov    rbx,QWORD PTR [rsp+0x4d0]
 1207d82:	00 
 1207d83:	48 8d 0d 9e 3b 94 00 	lea    rcx,[rip+0x943b9e]        # 1b4b928 <cbPAMConv@@Base+0x5dc778>
 1207d8a:	bf 01 00 00 00       	mov    edi,0x1
 1207d8f:	31 f6                	xor    esi,esi
 1207d91:	49 c7 c0 ff ff ff ff 	mov    r8,0xffffffffffffffff
 1207d98:	e8 c3 2b 32 ff       	call   52a960 <_cgo_topofstack@@Base+0xa7840>
 1207d9d:	0f 1f 00             	nop    DWORD PTR [rax]
 1207da0:	e9 85 0a 00 00       	jmp    120882a <crosscall2@@Base+0xc6070a>
 1207da5:	48 8b 94 24 a0 03 00 	mov    rdx,QWORD PTR [rsp+0x3a0]
 1207dac:	00 
 1207dad:	4c 8b 8c 24 a8 03 00 	mov    r9,QWORD PTR [rsp+0x3a8]
 1207db4:	00 
 1207db5:	eb 09                	jmp    1207dc0 <crosscall2@@Base+0xc5fca0>
 1207db7:	48 83 c2 48          	add    rdx,0x48
 1207dbb:	49 ff c9             	dec    r9
 1207dbe:	66 90                	xchg   ax,ax
 1207dc0:	4d 85 c9             	test   r9,r9
 1207dc3:	0f 8e a8 00 00 00    	jle    1207e71 <crosscall2@@Base+0xc5fd51>
 1207dc9:	4c 8b 12             	mov    r10,QWORD PTR [rdx]
 1207dcc:	4c 89 94 24 a8 04 00 	mov    QWORD PTR [rsp+0x4a8],r10
 1207dd3:	00 
 1207dd4:	0f 10 42 08          	movups xmm0,XMMWORD PTR [rdx+0x8]
 1207dd8:	0f 11 84 24 b0 04 00 	movups XMMWORD PTR [rsp+0x4b0],xmm0
 1207ddf:	00 
 1207de0:	0f 10 42 18          	movups xmm0,XMMWORD PTR [rdx+0x18]
 1207de4:	0f 11 84 24 c0 04 00 	movups XMMWORD PTR [rsp+0x4c0],xmm0
 1207deb:	00 
 1207dec:	0f 10 42 28          	movups xmm0,XMMWORD PTR [rdx+0x28]
 1207df0:	0f 11 84 24 d0 04 00 	movups XMMWORD PTR [rsp+0x4d0],xmm0
 1207df7:	00 
 1207df8:	0f 10 42 38          	movups xmm0,XMMWORD PTR [rdx+0x38]
 1207dfc:	0f 11 84 24 e0 04 00 	movups XMMWORD PTR [rsp+0x4e0],xmm0
 1207e03:	00 
 1207e04:	48 83 bc 24 c0 04 00 	cmp    QWORD PTR [rsp+0x4c0],0x7
 1207e0b:	00 07 
 1207e0d:	75 a8                	jne    1207db7 <crosscall2@@Base+0xc5fc97>
 1207e0f:	4c 8b 94 24 b8 04 00 	mov    r10,QWORD PTR [rsp+0x4b8]
 1207e16:	00 
 1207e17:	41 81 3a 73 79 73 70 	cmp    DWORD PTR [r10],0x70737973
 1207e1e:	66 90                	xchg   ax,ax
 1207e20:	75 95                	jne    1207db7 <crosscall2@@Base+0xc5fc97>
 1207e22:	66 41 81 7a 04 61 74 	cmp    WORD PTR [r10+0x4],0x7461
 1207e29:	75 8c                	jne    1207db7 <crosscall2@@Base+0xc5fc97>
 1207e2b:	41 80 7a 06 68       	cmp    BYTE PTR [r10+0x6],0x68
 1207e30:	75 85                	jne    1207db7 <crosscall2@@Base+0xc5fc97>
 1207e32:	4c 89 8c 24 d8 01 00 	mov    QWORD PTR [rsp+0x1d8],r9
 1207e39:	00 
 1207e3a:	48 89 94 24 08 04 00 	mov    QWORD PTR [rsp+0x408],rdx
 1207e41:	00 
 1207e42:	48 8b 84 24 c8 04 00 	mov    rax,QWORD PTR [rsp+0x4c8]
 1207e49:	00 
 1207e4a:	48 8b 9c 24 d0 04 00 	mov    rbx,QWORD PTR [rsp+0x4d0]
 1207e51:	00 
 1207e52:	48 8d 0d cf 3a 94 00 	lea    rcx,[rip+0x943acf]        # 1b4b928 <cbPAMConv@@Base+0x5dc778>
 1207e59:	bf 01 00 00 00       	mov    edi,0x1
 1207e5e:	31 f6                	xor    esi,esi
 1207e60:	49 c7 c0 ff ff ff ff 	mov    r8,0xffffffffffffffff
 1207e67:	e8 f4 2a 32 ff       	call   52a960 <_cgo_topofstack@@Base+0xa7840>
 1207e6c:	e9 e9 08 00 00       	jmp    120875a <crosscall2@@Base+0xc6063a>
 1207e71:	48 8b 94 24 b8 03 00 	mov    rdx,QWORD PTR [rsp+0x3b8]
 1207e78:	00 
 1207e79:	4c 8b 8c 24 c0 03 00 	mov    r9,QWORD PTR [rsp+0x3c0]
 1207e80:	00 
 1207e81:	eb 07                	jmp    1207e8a <crosscall2@@Base+0xc5fd6a>
 1207e83:	48 83 c2 48          	add    rdx,0x48
 1207e87:	49 ff c9             	dec    r9
 1207e8a:	4d 85 c9             	test   r9,r9
 1207e8d:	0f 8e a6 00 00 00    	jle    1207f39 <crosscall2@@Base+0xc5fe19>
 1207e93:	4c 8b 12             	mov    r10,QWORD PTR [rdx]
 1207e96:	4c 89 94 24 a8 04 00 	mov    QWORD PTR [rsp+0x4a8],r10
 1207e9d:	00 
 1207e9e:	0f 10 42 08          	movups xmm0,XMMWORD PTR [rdx+0x8]
 1207ea2:	0f 11 84 24 b0 04 00 	movups XMMWORD PTR [rsp+0x4b0],xmm0
 1207ea9:	00 
 1207eaa:	0f 10 42 18          	movups xmm0,XMMWORD PTR [rdx+0x18]
 1207eae:	0f 11 84 24 c0 04 00 	movups XMMWORD PTR [rsp+0x4c0],xmm0
 1207eb5:	00 
 1207eb6:	0f 10 42 28          	movups xmm0,XMMWORD PTR [rdx+0x28]
 1207eba:	0f 11 84 24 d0 04 00 	movups XMMWORD PTR [rsp+0x4d0],xmm0
 1207ec1:	00 
 1207ec2:	0f 10 42 38          	movups xmm0,XMMWORD PTR [rdx+0x38]
 1207ec6:	0f 11 84 24 e0 04 00 	movups XMMWORD PTR [rsp+0x4e0],xmm0
 1207ecd:	00 
 1207ece:	48 83 bc 24 c0 04 00 	cmp    QWORD PTR [rsp+0x4c0],0x7
 1207ed5:	00 07 
 1207ed7:	75 aa                	jne    1207e83 <crosscall2@@Base+0xc5fd63>
 1207ed9:	4c 8b 94 24 b8 04 00 	mov    r10,QWORD PTR [rsp+0x4b8]
 1207ee0:	00 
 1207ee1:	41 81 3a 73 79 73 70 	cmp    DWORD PTR [r10],0x70737973
 1207ee8:	75 99                	jne    1207e83 <crosscall2@@Base+0xc5fd63>
 1207eea:	66 41 81 7a 04 61 74 	cmp    WORD PTR [r10+0x4],0x7461
 1207ef1:	75 90                	jne    1207e83 <crosscall2@@Base+0xc5fd63>
 1207ef3:	41 80 7a 06 68       	cmp    BYTE PTR [r10+0x6],0x68
 1207ef8:	75 89                	jne    1207e83 <crosscall2@@Base+0xc5fd63>
 1207efa:	4c 89 8c 24 d8 01 00 	mov    QWORD PTR [rsp+0x1d8],r9
 1207f01:	00 
 1207f02:	48 89 94 24 08 04 00 	mov    QWORD PTR [rsp+0x408],rdx
 1207f09:	00 
 1207f0a:	48 8b 84 24 c8 04 00 	mov    rax,QWORD PTR [rsp+0x4c8]
 1207f11:	00 
 1207f12:	48 8b 9c 24 d0 04 00 	mov    rbx,QWORD PTR [rsp+0x4d0]
 1207f19:	00 
 1207f1a:	48 8d 0d 07 3a 94 00 	lea    rcx,[rip+0x943a07]        # 1b4b928 <cbPAMConv@@Base+0x5dc778>
 1207f21:	bf 01 00 00 00       	mov    edi,0x1
 1207f26:	31 f6                	xor    esi,esi
 1207f28:	49 c7 c0 ff ff ff ff 	mov    r8,0xffffffffffffffff
 1207f2f:	e8 2c 2a 32 ff       	call   52a960 <_cgo_topofstack@@Base+0xa7840>
 1207f34:	e9 4f 07 00 00       	jmp    1208688 <crosscall2@@Base+0xc60568>
 1207f39:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1207f40:	00 
 1207f41:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1207f48:	00 
 1207f49:	48 8d 0d cf 86 6e 00 	lea    rcx,[rip+0x6e86cf]        # 18f061f <cbPAMConv@@Base+0x38146f>
 1207f50:	bf 03 00 00 00       	mov    edi,0x3
 1207f55:	e8 66 03 28 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 1207f5a:	66 0f 1f 44 00 00    	nop    WORD PTR [rax+rax*1+0x0]
 1207f60:	48 85 c0             	test   rax,rax
 1207f63:	0f 8c f6 00 00 00    	jl     120805f <crosscall2@@Base+0xc5ff3f>
 1207f69:	48 89 e7             	mov    rdi,rsp
 1207f6c:	48 8d b4 24 88 03 00 	lea    rsi,[rsp+0x388]
 1207f73:	00 
 1207f74:	66 0f 1f 84 00 00 00 	nop    WORD PTR [rax+rax*1+0x0]
 1207f7b:	00 00 
 1207f7d:	0f 1f 00             	nop    DWORD PTR [rax]
 1207f80:	48 89 6c 24 f0       	mov    QWORD PTR [rsp-0x10],rbp
 1207f85:	48 8d 6c 24 f0       	lea    rbp,[rsp-0x10]
 1207f8a:	e8 0f bc 27 ff       	call   483b9e <_cgo_topofstack@@Base+0xa7e>
 1207f8f:	48 8b 6d 00          	mov    rbp,QWORD PTR [rbp+0x0]
 1207f93:	48 8b 84 24 88 06 00 	mov    rax,QWORD PTR [rsp+0x688]
 1207f9a:	00 
 1207f9b:	48 8b 9c 24 90 06 00 	mov    rbx,QWORD PTR [rsp+0x690]
 1207fa2:	00 
 1207fa3:	48 8b 8c 24 98 06 00 	mov    rcx,QWORD PTR [rsp+0x698]
 1207faa:	00 
 1207fab:	48 8b bc 24 a0 06 00 	mov    rdi,QWORD PTR [rsp+0x6a0]
 1207fb2:	00 
 1207fb3:	e8 08 da ff ff       	call   12059c0 <crosscall2@@Base+0xc5d8a0>
 1207fb8:	48 89 84 24 a8 04 00 	mov    QWORD PTR [rsp+0x4a8],rax
 1207fbf:	00 
 1207fc0:	48 89 9c 24 b0 04 00 	mov    QWORD PTR [rsp+0x4b0],rbx
 1207fc7:	00 
 1207fc8:	48 89 8c 24 b8 04 00 	mov    QWORD PTR [rsp+0x4b8],rcx
 1207fcf:	00 
 1207fd0:	48 89 bc 24 c0 04 00 	mov    QWORD PTR [rsp+0x4c0],rdi
 1207fd7:	00 
 1207fd8:	48 89 b4 24 c8 04 00 	mov    QWORD PTR [rsp+0x4c8],rsi
 1207fdf:	00 
 1207fe0:	4c 89 84 24 d0 04 00 	mov    QWORD PTR [rsp+0x4d0],r8
 1207fe7:	00 
 1207fe8:	44 88 8c 24 d8 04 00 	mov    BYTE PTR [rsp+0x4d8],r9b
 1207fef:	00 
 1207ff0:	4c 89 94 24 e0 04 00 	mov    QWORD PTR [rsp+0x4e0],r10
 1207ff7:	00 
 1207ff8:	4c 89 9c 24 e8 04 00 	mov    QWORD PTR [rsp+0x4e8],r11
 1207fff:	00 
 1208000:	48 8b 94 24 a8 04 00 	mov    rdx,QWORD PTR [rsp+0x4a8]
 1208007:	00 
 1208008:	48 89 94 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rdx
 120800f:	00 
 1208010:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 1208017:	00 
 1208018:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 120801f:	00 
 1208020:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 1208027:	00 
 1208028:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 120802f:	00 
 1208030:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 1208037:	00 
 1208038:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 120803f:	00 
 1208040:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 1208047:	00 
 1208048:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 120804f:	00 
 1208050:	48 83 bc 24 48 06 00 	cmp    QWORD PTR [rsp+0x648],0x0
 1208057:	00 00 
 1208059:	0f 85 20 05 00 00    	jne    120857f <crosscall2@@Base+0xc6045f>
 120805f:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208066:	00 
 1208067:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 120806e:	00 
 120806f:	48 8d 0d 5d 02 6f 00 	lea    rcx,[rip+0x6f025d]        # 18f82d3 <cbPAMConv@@Base+0x389123>
 1208076:	bf 06 00 00 00       	mov    edi,0x6
 120807b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 1208080:	e8 3b 02 28 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 1208085:	48 85 c0             	test   rax,rax
 1208088:	0f 8c f1 00 00 00    	jl     120817f <crosscall2@@Base+0xc6005f>
 120808e:	48 89 e7             	mov    rdi,rsp
 1208091:	48 8d b4 24 88 03 00 	lea    rsi,[rsp+0x388]
 1208098:	00 
 1208099:	0f 1f 80 00 00 00 00 	nop    DWORD PTR [rax+0x0]
 12080a0:	48 89 6c 24 f0       	mov    QWORD PTR [rsp-0x10],rbp
 12080a5:	48 8d 6c 24 f0       	lea    rbp,[rsp-0x10]
 12080aa:	e8 ef ba 27 ff       	call   483b9e <_cgo_topofstack@@Base+0xa7e>
 12080af:	48 8b 6d 00          	mov    rbp,QWORD PTR [rbp+0x0]
 12080b3:	48 8b 84 24 88 06 00 	mov    rax,QWORD PTR [rsp+0x688]
 12080ba:	00 
 12080bb:	48 8b 9c 24 90 06 00 	mov    rbx,QWORD PTR [rsp+0x690]
 12080c2:	00 
 12080c3:	48 8b 8c 24 98 06 00 	mov    rcx,QWORD PTR [rsp+0x698]
 12080ca:	00 
 12080cb:	48 8b bc 24 a0 06 00 	mov    rdi,QWORD PTR [rsp+0x6a0]
 12080d2:	00 
 12080d3:	e8 e8 d8 ff ff       	call   12059c0 <crosscall2@@Base+0xc5d8a0>
 12080d8:	48 89 84 24 a8 04 00 	mov    QWORD PTR [rsp+0x4a8],rax
 12080df:	00 
 12080e0:	48 89 9c 24 b0 04 00 	mov    QWORD PTR [rsp+0x4b0],rbx
 12080e7:	00 
 12080e8:	48 89 8c 24 b8 04 00 	mov    QWORD PTR [rsp+0x4b8],rcx
 12080ef:	00 
 12080f0:	48 89 bc 24 c0 04 00 	mov    QWORD PTR [rsp+0x4c0],rdi
 12080f7:	00 
 12080f8:	48 89 b4 24 c8 04 00 	mov    QWORD PTR [rsp+0x4c8],rsi
 12080ff:	00 
 1208100:	4c 89 84 24 d0 04 00 	mov    QWORD PTR [rsp+0x4d0],r8
 1208107:	00 
 1208108:	44 88 8c 24 d8 04 00 	mov    BYTE PTR [rsp+0x4d8],r9b
 120810f:	00 
 1208110:	4c 89 94 24 e0 04 00 	mov    QWORD PTR [rsp+0x4e0],r10
 1208117:	00 
 1208118:	4c 89 9c 24 e8 04 00 	mov    QWORD PTR [rsp+0x4e8],r11
 120811f:	00 
 1208120:	48 8b 94 24 a8 04 00 	mov    rdx,QWORD PTR [rsp+0x4a8]
 1208127:	00 
 1208128:	48 89 94 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rdx
 120812f:	00 
 1208130:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 1208137:	00 
 1208138:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 120813f:	00 
 1208140:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 1208147:	00 
 1208148:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 120814f:	00 
 1208150:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 1208157:	00 
 1208158:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 120815f:	00 
 1208160:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 1208167:	00 
 1208168:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 120816f:	00 
 1208170:	48 83 bc 24 48 06 00 	cmp    QWORD PTR [rsp+0x648],0x0
 1208177:	00 00 
 1208179:	0f 85 d4 03 00 00    	jne    1208553 <crosscall2@@Base+0xc60433>
 120817f:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208186:	00 
 1208187:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 120818e:	00 
 120818f:	48 8d 0d c9 91 6e 00 	lea    rcx,[rip+0x6e91c9]        # 18f135f <cbPAMConv@@Base+0x3821af>
 1208196:	bf 04 00 00 00       	mov    edi,0x4
 120819b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 12081a0:	e8 1b 01 28 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 12081a5:	48 85 c0             	test   rax,rax
 12081a8:	0f 8c 73 01 00 00    	jl     1208321 <crosscall2@@Base+0xc60201>
 12081ae:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 12081b5:	00 
 12081b6:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 12081bd:	00 
 12081be:	66 90                	xchg   ax,ax
 12081c0:	e8 9b 71 ff ff       	call   11ff360 <crosscall2@@Base+0xc57240>
 12081c5:	84 c0                	test   al,al
 12081c7:	0f 85 2b 01 00 00    	jne    12082f8 <crosscall2@@Base+0xc601d8>
 12081cd:	48 89 e7             	mov    rdi,rsp
 12081d0:	48 8d b4 24 88 03 00 	lea    rsi,[rsp+0x388]
 12081d7:	00 
 12081d8:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 12081df:	00 
 12081e0:	48 89 6c 24 f0       	mov    QWORD PTR [rsp-0x10],rbp
 12081e5:	48 8d 6c 24 f0       	lea    rbp,[rsp-0x10]
 12081ea:	e8 af b9 27 ff       	call   483b9e <_cgo_topofstack@@Base+0xa7e>
 12081ef:	48 8b 6d 00          	mov    rbp,QWORD PTR [rbp+0x0]
 12081f3:	48 8b 84 24 88 06 00 	mov    rax,QWORD PTR [rsp+0x688]
 12081fa:	00 
 12081fb:	48 8b 9c 24 90 06 00 	mov    rbx,QWORD PTR [rsp+0x690]
 1208202:	00 
 1208203:	48 8b 8c 24 98 06 00 	mov    rcx,QWORD PTR [rsp+0x698]
 120820a:	00 
 120820b:	48 8b bc 24 a0 06 00 	mov    rdi,QWORD PTR [rsp+0x6a0]
 1208212:	00 
 1208213:	e8 28 da ff ff       	call   1205c40 <crosscall2@@Base+0xc5db20>
 1208218:	48 89 84 24 a8 04 00 	mov    QWORD PTR [rsp+0x4a8],rax
 120821f:	00 
 1208220:	48 89 9c 24 b0 04 00 	mov    QWORD PTR [rsp+0x4b0],rbx
 1208227:	00 
 1208228:	48 89 8c 24 b8 04 00 	mov    QWORD PTR [rsp+0x4b8],rcx
 120822f:	00 
 1208230:	48 89 bc 24 c0 04 00 	mov    QWORD PTR [rsp+0x4c0],rdi
 1208237:	00 
 1208238:	48 89 b4 24 c8 04 00 	mov    QWORD PTR [rsp+0x4c8],rsi
 120823f:	00 
 1208240:	4c 89 84 24 d0 04 00 	mov    QWORD PTR [rsp+0x4d0],r8
 1208247:	00 
 1208248:	44 88 8c 24 d8 04 00 	mov    BYTE PTR [rsp+0x4d8],r9b
 120824f:	00 
 1208250:	4c 89 94 24 e0 04 00 	mov    QWORD PTR [rsp+0x4e0],r10
 1208257:	00 
 1208258:	4c 89 9c 24 e8 04 00 	mov    QWORD PTR [rsp+0x4e8],r11
 120825f:	00 
 1208260:	48 8b 94 24 a8 04 00 	mov    rdx,QWORD PTR [rsp+0x4a8]
 1208267:	00 
 1208268:	48 89 94 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rdx
 120826f:	00 
 1208270:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 1208277:	00 
 1208278:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 120827f:	00 
 1208280:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 1208287:	00 
 1208288:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 120828f:	00 
 1208290:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 1208297:	00 
 1208298:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 120829f:	00 
 12082a0:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 12082a7:	00 
 12082a8:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 12082af:	00 
 12082b0:	48 83 bc 24 48 06 00 	cmp    QWORD PTR [rsp+0x648],0x0
 12082b7:	00 00 
 12082b9:	75 2f                	jne    12082ea <crosscall2@@Base+0xc601ca>
 12082bb:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 12082c2:	00 
 12082c3:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 12082ca:	00 
 12082cb:	48 8d 0d 2e 7a 94 00 	lea    rcx,[rip+0x947a2e]        # 1b4fd00 <cbPAMConv@@Base+0x5e0b50>
 12082d2:	bf 01 00 00 00       	mov    edi,0x1
 12082d7:	31 f6                	xor    esi,esi
 12082d9:	49 c7 c0 ff ff ff ff 	mov    r8,0xffffffffffffffff
 12082e0:	e8 7b 26 32 ff       	call   52a960 <_cgo_topofstack@@Base+0xa7840>
 12082e5:	e9 d8 02 00 00       	jmp    12085c2 <crosscall2@@Base+0xc604a2>
 12082ea:	b8 02 00 00 00       	mov    eax,0x2
 12082ef:	48 81 c4 30 06 00 00 	add    rsp,0x630
 12082f6:	5d                   	pop    rbp
 12082f7:	c3                   	ret
 12082f8:	48 8d 0d 23 83 6e 00 	lea    rcx,[rip+0x6e8323]        # 18f0622 <cbPAMConv@@Base+0x381472>
 12082ff:	48 89 8c 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rcx
 1208306:	00 
 1208307:	48 c7 84 24 48 06 00 	mov    QWORD PTR [rsp+0x648],0x3
 120830e:	00 03 00 00 00 
 1208313:	b8 0a 00 00 00       	mov    eax,0xa
 1208318:	48 81 c4 30 06 00 00 	add    rsp,0x630
 120831f:	5d                   	pop    rbp
 1208320:	c3                   	ret
 1208321:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208328:	00 
 1208329:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1208330:	00 
 1208331:	48 8d 0d e4 82 6e 00 	lea    rcx,[rip+0x6e82e4]        # 18f061c <cbPAMConv@@Base+0x38146c>
 1208338:	bf 03 00 00 00       	mov    edi,0x3
 120833d:	0f 1f 00             	nop    DWORD PTR [rax]
 1208340:	e8 7b ff 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 1208345:	48 85 c0             	test   rax,rax
 1208348:	0f 8c 9f 01 00 00    	jl     12084ed <crosscall2@@Base+0xc603cd>
 120834e:	48 8b bc 24 d8 03 00 	mov    rdi,QWORD PTR [rsp+0x3d8]
 1208355:	00 
 1208356:	48 85 ff             	test   rdi,rdi
 1208359:	74 2e                	je     1208389 <crosscall2@@Base+0xc60269>
 120835b:	48 8b 8c 24 d0 03 00 	mov    rcx,QWORD PTR [rsp+0x3d0]
 1208362:	00 
 1208363:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 120836a:	00 
 120836b:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1208372:	00 
 1208373:	e8 48 ff 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 1208378:	0f 1f 84 00 00 00 00 	nop    DWORD PTR [rax+rax*1+0x0]
 120837f:	00 
 1208380:	48 85 c0             	test   rax,rax
 1208383:	0f 8d 56 01 00 00    	jge    12084df <crosscall2@@Base+0xc603bf>
 1208389:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208390:	00 
 1208391:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1208398:	00 
 1208399:	e8 c2 a9 ff ff       	call   1202d60 <crosscall2@@Base+0xc5ac40>
 120839e:	66 90                	xchg   ax,ax
 12083a0:	84 c0                	test   al,al
 12083a2:	74 41                	je     12083e5 <crosscall2@@Base+0xc602c5>
 12083a4:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 12083ab:	00 
 12083ac:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 12083b3:	00 
 12083b4:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 12083bb:	00 
 12083bc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 12083c0:	e8 7b 08 00 00       	call   1208c40 <crosscall2@@Base+0xc60b20>
 12083c5:	0f b6 d0             	movzx  edx,al
 12083c8:	48 85 d2             	test   rdx,rdx
 12083cb:	ba 0c 00 00 00       	mov    edx,0xc
 12083d0:	be 0b 00 00 00       	mov    esi,0xb
 12083d5:	48 0f 45 d6          	cmovne rdx,rsi
 12083d9:	48 89 d0             	mov    rax,rdx
 12083dc:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 12083e0:	e9 9f 00 00 00       	jmp    1208484 <crosscall2@@Base+0xc60364>
 12083e5:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 12083ec:	00 
 12083ed:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 12083f4:	00 
 12083f5:	e8 86 e1 ff ff       	call   1206580 <crosscall2@@Base+0xc5e460>
 12083fa:	84 c0                	test   al,al
 12083fc:	74 07                	je     1208405 <crosscall2@@Base+0xc602e5>
 12083fe:	b8 05 00 00 00       	mov    eax,0x5
 1208403:	eb 7f                	jmp    1208484 <crosscall2@@Base+0xc60364>
 1208405:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 120840c:	00 
 120840d:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 1208414:	00 
 1208415:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 120841c:	00 
 120841d:	0f 1f 00             	nop    DWORD PTR [rax]
 1208420:	e8 1b 08 00 00       	call   1208c40 <crosscall2@@Base+0xc60b20>
 1208425:	84 c0                	test   al,al
 1208427:	74 07                	je     1208430 <crosscall2@@Base+0xc60310>
 1208429:	b8 03 00 00 00       	mov    eax,0x3
 120842e:	eb 54                	jmp    1208484 <crosscall2@@Base+0xc60364>
 1208430:	0f b6 8c 24 a8 06 00 	movzx  ecx,BYTE PTR [rsp+0x6a8]
 1208437:	00 
 1208438:	84 c9                	test   cl,cl
 120843a:	74 07                	je     1208443 <crosscall2@@Base+0xc60323>
 120843c:	b8 04 00 00 00       	mov    eax,0x4
 1208441:	eb 41                	jmp    1208484 <crosscall2@@Base+0xc60364>
 1208443:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 120844a:	00 
 120844b:	48 85 c9             	test   rcx,rcx
 120844e:	75 07                	jne    1208457 <crosscall2@@Base+0xc60337>
 1208450:	b8 05 00 00 00       	mov    eax,0x5
 1208455:	eb 2d                	jmp    1208484 <crosscall2@@Base+0xc60364>
 1208457:	48 8b 81 b0 00 00 00 	mov    rax,QWORD PTR [rcx+0xb0]
 120845e:	48 8b 99 b8 00 00 00 	mov    rbx,QWORD PTR [rcx+0xb8]
 1208465:	e8 d6 3f 32 ff       	call   52c440 <_cgo_topofstack@@Base+0xa9320>
 120846a:	48 83 fb 04          	cmp    rbx,0x4
 120846e:	75 0f                	jne    120847f <crosscall2@@Base+0xc6035f>
 1208470:	81 38 6e 76 6d 65    	cmp    DWORD PTR [rax],0x656d766e
 1208476:	75 07                	jne    120847f <crosscall2@@Base+0xc6035f>
 1208478:	b8 06 00 00 00       	mov    eax,0x6
 120847d:	eb 05                	jmp    1208484 <crosscall2@@Base+0xc60364>
 120847f:	b8 04 00 00 00       	mov    eax,0x4
 1208484:	48 89 84 24 d0 01 00 	mov    QWORD PTR [rsp+0x1d0],rax
 120848b:	00 
 120848c:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1208493:	00 
 1208494:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 120849b:	00 
 120849c:	0f 1f 40 00          	nop    DWORD PTR [rax+0x0]
 12084a0:	e8 9b 9f cb ff       	call   ec2440 <crosscall2@@Base+0x91a320>
 12084a5:	b9 03 00 00 00       	mov    ecx,0x3
 12084aa:	48 89 c7             	mov    rdi,rax
 12084ad:	48 89 de             	mov    rsi,rbx
 12084b0:	31 c0                	xor    eax,eax
 12084b2:	48 8d 1d 63 81 6e 00 	lea    rbx,[rip+0x6e8163]        # 18f061c <cbPAMConv@@Base+0x38146c>
 12084b9:	e8 a2 65 25 ff       	call   45ea60 <pam_start_confdir@plt+0x58e48>
 12084be:	48 89 84 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rax
 12084c5:	00 
 12084c6:	48 89 9c 24 48 06 00 	mov    QWORD PTR [rsp+0x648],rbx
 12084cd:	00 
 12084ce:	48 8b 84 24 d0 01 00 	mov    rax,QWORD PTR [rsp+0x1d0]
 12084d5:	00 
 12084d6:	48 81 c4 30 06 00 00 	add    rsp,0x630
 12084dd:	5d                   	pop    rbp
 12084de:	c3                   	ret
 12084df:	b8 07 00 00 00       	mov    eax,0x7
 12084e4:	48 81 c4 30 06 00 00 	add    rsp,0x630
 12084eb:	5d                   	pop    rbp
 12084ec:	c3                   	ret
 12084ed:	44 0f 11 bc 24 78 04 	movups XMMWORD PTR [rsp+0x478],xmm15
 12084f4:	00 00 
 12084f6:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 12084fd:	00 
 12084fe:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 1208505:	00 
 1208506:	e8 15 c9 26 ff       	call   474e20 <pam_start_confdir@plt+0x6f208>
 120850b:	48 8d 0d 2e 7d 43 00 	lea    rcx,[rip+0x437d2e]        # 1640240 <cbPAMConv@@Base+0xd1090>
 1208512:	48 89 8c 24 78 04 00 	mov    QWORD PTR [rsp+0x478],rcx
 1208519:	00 
 120851a:	48 89 84 24 80 04 00 	mov    QWORD PTR [rsp+0x480],rax
 1208521:	00 
 1208522:	48 8d 05 95 44 71 00 	lea    rax,[rip+0x714495]        # 191c9be <cbPAMConv@@Base+0x3ad80e>
 1208529:	bb 19 00 00 00       	mov    ebx,0x19
 120852e:	48 8d 8c 24 78 04 00 	lea    rcx,[rsp+0x478]
 1208535:	00 
 1208536:	bf 01 00 00 00       	mov    edi,0x1
 120853b:	48 89 fe             	mov    rsi,rdi
 120853e:	66 90                	xchg   ax,ax
 1208540:	e8 3b 0d 77 ff       	call   979280 <crosscall2@@Base+0x3d1160>
 1208545:	b8 08 00 00 00       	mov    eax,0x8
 120854a:	48 81 c4 30 06 00 00 	add    rsp,0x630
 1208551:	5d                   	pop    rbp
 1208552:	c3                   	ret
 1208553:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 120855a:	00 
 120855b:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 1208562:	00 
 1208563:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 120856a:	00 
 120856b:	e8 d0 06 00 00       	call   1208c40 <crosscall2@@Base+0xc60b20>
 1208570:	83 f0 01             	xor    eax,0x1
 1208573:	0f b6 c0             	movzx  eax,al
 1208576:	48 81 c4 30 06 00 00 	add    rsp,0x630
 120857d:	5d                   	pop    rbp
 120857e:	c3                   	ret
 120857f:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 1208586:	00 
 1208587:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 120858e:	00 
 120858f:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 1208596:	00 
 1208597:	e8 a4 06 00 00       	call   1208c40 <crosscall2@@Base+0xc60b20>
 120859c:	83 f0 01             	xor    eax,0x1
 120859f:	0f b6 c0             	movzx  eax,al
 12085a2:	48 81 c4 30 06 00 00 	add    rsp,0x630
 12085a9:	5d                   	pop    rbp
 12085aa:	c3                   	ret
 12085ab:	48 8b 84 24 08 04 00 	mov    rax,QWORD PTR [rsp+0x408]
 12085b2:	00 
 12085b3:	48 83 c0 10          	add    rax,0x10
 12085b7:	48 8b 9c 24 d8 01 00 	mov    rbx,QWORD PTR [rsp+0x1d8]
 12085be:	00 
 12085bf:	48 ff cb             	dec    rbx
 12085c2:	48 85 db             	test   rbx,rbx
 12085c5:	7e 69                	jle    1208630 <crosscall2@@Base+0xc60510>
 12085c7:	48 89 9c 24 d8 01 00 	mov    QWORD PTR [rsp+0x1d8],rbx
 12085ce:	00 
 12085cf:	48 89 84 24 08 04 00 	mov    QWORD PTR [rsp+0x408],rax
 12085d6:	00 
 12085d7:	48 8b 58 08          	mov    rbx,QWORD PTR [rax+0x8]
 12085db:	48 89 9c 24 b8 01 00 	mov    QWORD PTR [rsp+0x1b8],rbx
 12085e2:	00 
 12085e3:	48 8b 10             	mov    rdx,QWORD PTR [rax]
 12085e6:	48 89 94 24 f0 01 00 	mov    QWORD PTR [rsp+0x1f0],rdx
 12085ed:	00 
 12085ee:	48 8d 0d 6a 8d 6e 00 	lea    rcx,[rip+0x6e8d6a]        # 18f135f <cbPAMConv@@Base+0x3821af>
 12085f5:	bf 04 00 00 00       	mov    edi,0x4
 12085fa:	48 89 d0             	mov    rax,rdx
 12085fd:	0f 1f 00             	nop    DWORD PTR [rax]
 1208600:	e8 bb fc 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 1208605:	48 85 c0             	test   rax,rax
 1208608:	7c a1                	jl     12085ab <crosscall2@@Base+0xc6048b>
 120860a:	48 8b 94 24 b8 01 00 	mov    rdx,QWORD PTR [rsp+0x1b8]
 1208611:	00 
 1208612:	48 83 fa 05          	cmp    rdx,0x5
 1208616:	75 93                	jne    12085ab <crosscall2@@Base+0xc6048b>
 1208618:	4c 8b 84 24 f0 01 00 	mov    r8,QWORD PTR [rsp+0x1f0]
 120861f:	00 
 1208620:	4c 89 84 24 40 06 00 	mov    QWORD PTR [rsp+0x640],r8
 1208627:	00 
 1208628:	48 89 94 24 48 06 00 	mov    QWORD PTR [rsp+0x648],rdx
 120862f:	00 
 1208630:	48 8b bc 24 40 06 00 	mov    rdi,QWORD PTR [rsp+0x640]
 1208637:	00 
 1208638:	48 8b b4 24 48 06 00 	mov    rsi,QWORD PTR [rsp+0x648]
 120863f:	00 
 1208640:	31 c0                	xor    eax,eax
 1208642:	48 8d 1d dc 7f 6e 00 	lea    rbx,[rip+0x6e7fdc]        # 18f0625 <cbPAMConv@@Base+0x381475>
 1208649:	b9 03 00 00 00       	mov    ecx,0x3
 120864e:	e8 0d 64 25 ff       	call   45ea60 <pam_start_confdir@plt+0x58e48>
 1208653:	48 89 84 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rax
 120865a:	00 
 120865b:	48 89 9c 24 48 06 00 	mov    QWORD PTR [rsp+0x648],rbx
 1208662:	00 
 1208663:	b8 09 00 00 00       	mov    eax,0x9
 1208668:	48 81 c4 30 06 00 00 	add    rsp,0x630
 120866f:	5d                   	pop    rbp
 1208670:	c3                   	ret
 1208671:	48 8b 84 24 00 04 00 	mov    rax,QWORD PTR [rsp+0x400]
 1208678:	00 
 1208679:	48 83 c0 10          	add    rax,0x10
 120867d:	48 8b 9c 24 c8 01 00 	mov    rbx,QWORD PTR [rsp+0x1c8]
 1208684:	00 
 1208685:	48 ff cb             	dec    rbx
 1208688:	48 85 db             	test   rbx,rbx
 120868b:	7e 58                	jle    12086e5 <crosscall2@@Base+0xc605c5>
 120868d:	48 89 9c 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rbx
 1208694:	00 
 1208695:	48 89 84 24 00 04 00 	mov    QWORD PTR [rsp+0x400],rax
 120869c:	00 
 120869d:	48 8b 08             	mov    rcx,QWORD PTR [rax]
 12086a0:	48 8b 78 08          	mov    rdi,QWORD PTR [rax+0x8]
 12086a4:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 12086ab:	00 
 12086ac:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 12086b3:	00 
 12086b4:	e8 07 fc 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 12086b9:	48 85 c0             	test   rax,rax
 12086bc:	7d b3                	jge    1208671 <crosscall2@@Base+0xc60551>
 12086be:	48 8b 84 24 f8 01 00 	mov    rax,QWORD PTR [rsp+0x1f8]
 12086c5:	00 
 12086c6:	0f b6 8c 24 a8 06 00 	movzx  ecx,BYTE PTR [rsp+0x6a8]
 12086cd:	00 
 12086ce:	48 8b 94 24 08 04 00 	mov    rdx,QWORD PTR [rsp+0x408]
 12086d5:	00 
 12086d6:	4c 8b 8c 24 d8 01 00 	mov    r9,QWORD PTR [rsp+0x1d8]
 12086dd:	00 
 12086de:	66 90                	xchg   ax,ax
 12086e0:	e9 9e f7 ff ff       	jmp    1207e83 <crosscall2@@Base+0xc5fd63>
 12086e5:	48 8b 8c 24 a8 04 00 	mov    rcx,QWORD PTR [rsp+0x4a8]
 12086ec:	00 
 12086ed:	48 89 8c 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rcx
 12086f4:	00 
 12086f5:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 12086fc:	00 
 12086fd:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 1208704:	00 
 1208705:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 120870c:	00 
 120870d:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 1208714:	00 
 1208715:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 120871c:	00 
 120871d:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 1208724:	00 
 1208725:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 120872c:	00 
 120872d:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 1208734:	00 
 1208735:	b8 02 00 00 00       	mov    eax,0x2
 120873a:	48 81 c4 30 06 00 00 	add    rsp,0x630
 1208741:	5d                   	pop    rbp
 1208742:	c3                   	ret
 1208743:	48 8b 84 24 00 04 00 	mov    rax,QWORD PTR [rsp+0x400]
 120874a:	00 
 120874b:	48 83 c0 10          	add    rax,0x10
 120874f:	48 8b 9c 24 c8 01 00 	mov    rbx,QWORD PTR [rsp+0x1c8]
 1208756:	00 
 1208757:	48 ff cb             	dec    rbx
 120875a:	48 85 db             	test   rbx,rbx
 120875d:	7e 56                	jle    12087b5 <crosscall2@@Base+0xc60695>
 120875f:	48 89 9c 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rbx
 1208766:	00 
 1208767:	48 89 84 24 00 04 00 	mov    QWORD PTR [rsp+0x400],rax
 120876e:	00 
 120876f:	48 8b 08             	mov    rcx,QWORD PTR [rax]
 1208772:	48 8b 78 08          	mov    rdi,QWORD PTR [rax+0x8]
 1208776:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 120877d:	00 
 120877e:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208785:	00 
 1208786:	e8 35 fb 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 120878b:	48 85 c0             	test   rax,rax
 120878e:	7d b3                	jge    1208743 <crosscall2@@Base+0xc60623>
 1208790:	48 8b 84 24 f8 01 00 	mov    rax,QWORD PTR [rsp+0x1f8]
 1208797:	00 
 1208798:	0f b6 8c 24 a8 06 00 	movzx  ecx,BYTE PTR [rsp+0x6a8]
 120879f:	00 
 12087a0:	48 8b 94 24 08 04 00 	mov    rdx,QWORD PTR [rsp+0x408]
 12087a7:	00 
 12087a8:	4c 8b 8c 24 d8 01 00 	mov    r9,QWORD PTR [rsp+0x1d8]
 12087af:	00 
 12087b0:	e9 02 f6 ff ff       	jmp    1207db7 <crosscall2@@Base+0xc5fc97>
 12087b5:	48 8b 8c 24 a8 04 00 	mov    rcx,QWORD PTR [rsp+0x4a8]
 12087bc:	00 
 12087bd:	48 89 8c 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rcx
 12087c4:	00 
 12087c5:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 12087cc:	00 
 12087cd:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 12087d4:	00 
 12087d5:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 12087dc:	00 
 12087dd:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 12087e4:	00 
 12087e5:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 12087ec:	00 
 12087ed:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 12087f4:	00 
 12087f5:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 12087fc:	00 
 12087fd:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 1208804:	00 
 1208805:	b8 02 00 00 00       	mov    eax,0x2
 120880a:	48 81 c4 30 06 00 00 	add    rsp,0x630
 1208811:	5d                   	pop    rbp
 1208812:	c3                   	ret
 1208813:	48 8b 84 24 00 04 00 	mov    rax,QWORD PTR [rsp+0x400]
 120881a:	00 
 120881b:	48 83 c0 10          	add    rax,0x10
 120881f:	48 8b 9c 24 c8 01 00 	mov    rbx,QWORD PTR [rsp+0x1c8]
 1208826:	00 
 1208827:	48 ff cb             	dec    rbx
 120882a:	48 85 db             	test   rbx,rbx
 120882d:	7e 41                	jle    1208870 <crosscall2@@Base+0xc60750>
 120882f:	48 89 9c 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rbx
 1208836:	00 
 1208837:	48 89 84 24 00 04 00 	mov    QWORD PTR [rsp+0x400],rax
 120883e:	00 
 120883f:	48 8b 08             	mov    rcx,QWORD PTR [rax]
 1208842:	48 8b 78 08          	mov    rdi,QWORD PTR [rax+0x8]
 1208846:	48 8b 9c 24 a0 06 00 	mov    rbx,QWORD PTR [rsp+0x6a0]
 120884d:	00 
 120884e:	48 8b 84 24 98 06 00 	mov    rax,QWORD PTR [rsp+0x698]
 1208855:	00 
 1208856:	e8 65 fa 27 ff       	call   4882c0 <_cgo_topofstack@@Base+0x51a0>
 120885b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 1208860:	48 85 c0             	test   rax,rax
 1208863:	7d ae                	jge    1208813 <crosscall2@@Base+0xc606f3>
 1208865:	48 8b 94 24 c8 01 00 	mov    rdx,QWORD PTR [rsp+0x1c8]
 120886c:	00 
 120886d:	48 85 d2             	test   rdx,rdx
 1208870:	7e 25                	jle    1208897 <crosscall2@@Base+0xc60777>
 1208872:	48 8b 84 24 f8 01 00 	mov    rax,QWORD PTR [rsp+0x1f8]
 1208879:	00 
 120887a:	0f b6 8c 24 a8 06 00 	movzx  ecx,BYTE PTR [rsp+0x6a8]
 1208881:	00 
 1208882:	48 8b 94 24 08 04 00 	mov    rdx,QWORD PTR [rsp+0x408]
 1208889:	00 
 120888a:	4c 8b 8c 24 d8 01 00 	mov    r9,QWORD PTR [rsp+0x1d8]
 1208891:	00 
 1208892:	e9 54 f4 ff ff       	jmp    1207ceb <crosscall2@@Base+0xc5fbcb>
 1208897:	48 8b 94 24 a8 04 00 	mov    rdx,QWORD PTR [rsp+0x4a8]
 120889e:	00 
 120889f:	48 89 94 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rdx
 12088a6:	00 
 12088a7:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 12088ae:	00 
 12088af:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 12088b6:	00 
 12088b7:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 12088be:	00 
 12088bf:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 12088c6:	00 
 12088c7:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 12088ce:	00 
 12088cf:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 12088d6:	00 
 12088d7:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 12088de:	00 
 12088df:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 12088e6:	00 
 12088e7:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 12088ee:	00 
 12088ef:	48 8b 9c 24 b0 01 00 	mov    rbx,QWORD PTR [rsp+0x1b0]
 12088f6:	00 
 12088f7:	48 8b 8c 24 f8 01 00 	mov    rcx,QWORD PTR [rsp+0x1f8]
 12088fe:	00 
 12088ff:	90                   	nop
 1208900:	e8 3b 03 00 00       	call   1208c40 <crosscall2@@Base+0xc60b20>
 1208905:	83 f0 01             	xor    eax,0x1
 1208908:	0f b6 c0             	movzx  eax,al
 120890b:	48 81 c4 30 06 00 00 	add    rsp,0x630
 1208912:	5d                   	pop    rbp
 1208913:	c3                   	ret
 1208914:	48 8b 84 24 00 04 00 	mov    rax,QWORD PTR [rsp+0x400]
 120891b:	00 
 120891c:	48 83 c0 10          	add    rax,0x10
 1208920:	48 8b 9c 24 c8 01 00 	mov    rbx,QWORD PTR [rsp+0x1c8]
 1208927:	00 
 1208928:	48 ff cb             	dec    rbx
 120892b:	48 85 db             	test   rbx,rbx
 120892e:	0f 8e 17 01 00 00    	jle    1208a4b <crosscall2@@Base+0xc6092b>
 1208934:	48 89 9c 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rbx
 120893b:	00 
 120893c:	48 89 84 24 00 04 00 	mov    QWORD PTR [rsp+0x400],rax
 1208943:	00 
 1208944:	48 8b 10             	mov    rdx,QWORD PTR [rax]
 1208947:	48 8b 70 08          	mov    rsi,QWORD PTR [rax+0x8]
 120894b:	44 0f 11 bc 24 18 04 	movups XMMWORD PTR [rsp+0x418],xmm15
 1208952:	00 00 
 1208954:	44 0f 11 bc 24 28 04 	movups XMMWORD PTR [rsp+0x428],xmm15
 120895b:	00 00 
 120895d:	48 c7 84 24 20 04 00 	mov    QWORD PTR [rsp+0x420],0x11
 1208964:	00 11 00 00 00 
 1208969:	48 8d 3d dc 48 70 00 	lea    rdi,[rip+0x7048dc]        # 190d24c <cbPAMConv@@Base+0x39e09c>
 1208970:	48 89 bc 24 18 04 00 	mov    QWORD PTR [rsp+0x418],rdi
 1208977:	00 
 1208978:	48 89 b4 24 30 04 00 	mov    QWORD PTR [rsp+0x430],rsi
 120897f:	00 
 1208980:	48 89 94 24 28 04 00 	mov    QWORD PTR [rsp+0x428],rdx
 1208987:	00 
 1208988:	bb 02 00 00 00       	mov    ebx,0x2
 120898d:	48 89 d9             	mov    rcx,rbx
 1208990:	48 8d 84 24 18 04 00 	lea    rax,[rsp+0x418]
 1208997:	00 
 1208998:	e8 a3 09 38 ff       	call   589340 <_cgo_topofstack@@Base+0x106220>
 120899d:	0f 1f 00             	nop    DWORD PTR [rax]
 12089a0:	e8 db 56 30 ff       	call   50e080 <_cgo_topofstack@@Base+0x8af60>
 12089a5:	48 85 c9             	test   rcx,rcx
 12089a8:	74 0d                	je     12089b7 <crosscall2@@Base+0xc60897>
 12089aa:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 12089b1:	00 
 12089b2:	e9 5d ff ff ff       	jmp    1208914 <crosscall2@@Base+0xc607f4>
 12089b7:	e8 04 3c 2f ff       	call   4fc5c0 <_cgo_topofstack@@Base+0x794a0>
 12089bc:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 12089c3:	00 
 12089c4:	48 39 cb             	cmp    rbx,rcx
 12089c7:	74 04                	je     12089cd <crosscall2@@Base+0xc608ad>
 12089c9:	31 c0                	xor    eax,eax
 12089cb:	eb 18                	jmp    12089e5 <crosscall2@@Base+0xc608c5>
 12089cd:	48 89 c3             	mov    rbx,rax
 12089d0:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 12089d7:	00 
 12089d8:	e8 e3 2b 20 ff       	call   40b5c0 <pam_start_confdir@plt+0x59a8>
 12089dd:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 12089e4:	00 
 12089e5:	84 c0                	test   al,al
 12089e7:	0f 84 27 ff ff ff    	je     1208914 <crosscall2@@Base+0xc607f4>
 12089ed:	48 8b 8c 24 a8 04 00 	mov    rcx,QWORD PTR [rsp+0x4a8]
 12089f4:	00 
 12089f5:	48 89 8c 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rcx
 12089fc:	00 
 12089fd:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 1208a04:	00 
 1208a05:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 1208a0c:	00 
 1208a0d:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 1208a14:	00 
 1208a15:	0f 11 84 24 58 06 00 	movups XMMWORD PTR [rsp+0x658],xmm0
 1208a1c:	00 
 1208a1d:	0f 10 84 24 d0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4d0]
 1208a24:	00 
 1208a25:	0f 11 84 24 68 06 00 	movups XMMWORD PTR [rsp+0x668],xmm0
 1208a2c:	00 
 1208a2d:	0f 10 84 24 e0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4e0]
 1208a34:	00 
 1208a35:	0f 11 84 24 78 06 00 	movups XMMWORD PTR [rsp+0x678],xmm0
 1208a3c:	00 
 1208a3d:	b8 02 00 00 00       	mov    eax,0x2
 1208a42:	48 81 c4 30 06 00 00 	add    rsp,0x630
 1208a49:	5d                   	pop    rbp
 1208a4a:	c3                   	ret
 1208a4b:	48 8b 84 24 f8 01 00 	mov    rax,QWORD PTR [rsp+0x1f8]
 1208a52:	00 
 1208a53:	0f b6 8c 24 a8 06 00 	movzx  ecx,BYTE PTR [rsp+0x6a8]
 1208a5a:	00 
 1208a5b:	48 8b 94 24 08 04 00 	mov    rdx,QWORD PTR [rsp+0x408]
 1208a62:	00 
 1208a63:	4c 8b 8c 24 d8 01 00 	mov    r9,QWORD PTR [rsp+0x1d8]
 1208a6a:	00 
 1208a6b:	49 bb 64 65 76 5f 62 	movabs r11,0x702d79625f766564
 1208a72:	79 2d 70 
 1208a75:	e9 91 f1 ff ff       	jmp    1207c0b <crosscall2@@Base+0xc5faeb>
 1208a7a:	48 8b 84 24 00 04 00 	mov    rax,QWORD PTR [rsp+0x400]
 1208a81:	00 
 1208a82:	48 83 c0 10          	add    rax,0x10
 1208a86:	48 8b 9c 24 c8 01 00 	mov    rbx,QWORD PTR [rsp+0x1c8]
 1208a8d:	00 
 1208a8e:	48 ff cb             	dec    rbx
 1208a91:	48 85 db             	test   rbx,rbx
 1208a94:	0f 8e 33 01 00 00    	jle    1208bcd <crosscall2@@Base+0xc60aad>
 1208a9a:	48 89 9c 24 c8 01 00 	mov    QWORD PTR [rsp+0x1c8],rbx
 1208aa1:	00 
 1208aa2:	48 89 84 24 00 04 00 	mov    QWORD PTR [rsp+0x400],rax
 1208aa9:	00 
 1208aaa:	48 8b 10             	mov    rdx,QWORD PTR [rax]
 1208aad:	48 8b 70 08          	mov    rsi,QWORD PTR [rax+0x8]
 1208ab1:	44 0f 11 bc 24 38 04 	movups XMMWORD PTR [rsp+0x438],xmm15
 1208ab8:	00 00 
 1208aba:	44 0f 11 bc 24 48 04 	movups XMMWORD PTR [rsp+0x448],xmm15
 1208ac1:	00 00 
 1208ac3:	48 c7 84 24 40 04 00 	mov    QWORD PTR [rsp+0x440],0x11
 1208aca:	00 11 00 00 00 
 1208acf:	48 8d 3d 76 47 70 00 	lea    rdi,[rip+0x704776]        # 190d24c <cbPAMConv@@Base+0x39e09c>
 1208ad6:	48 89 bc 24 38 04 00 	mov    QWORD PTR [rsp+0x438],rdi
 1208add:	00 
 1208ade:	48 89 b4 24 50 04 00 	mov    QWORD PTR [rsp+0x450],rsi
 1208ae5:	00 
 1208ae6:	48 89 94 24 48 04 00 	mov    QWORD PTR [rsp+0x448],rdx
 1208aed:	00 
 1208aee:	bb 02 00 00 00       	mov    ebx,0x2
 1208af3:	48 89 d9             	mov    rcx,rbx
 1208af6:	48 8d 84 24 38 04 00 	lea    rax,[rsp+0x438]
 1208afd:	00 
 1208afe:	66 90                	xchg   ax,ax
 1208b00:	e8 3b 08 38 ff       	call   589340 <_cgo_topofstack@@Base+0x106220>
 1208b05:	e8 76 55 30 ff       	call   50e080 <_cgo_topofstack@@Base+0x8af60>
 1208b0a:	48 85 c9             	test   rcx,rcx
 1208b0d:	74 0c                	je     1208b1b <crosscall2@@Base+0xc609fb>
 1208b0f:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 1208b16:	00 
 1208b17:	31 c0                	xor    eax,eax
 1208b19:	eb 33                	jmp    1208b4e <crosscall2@@Base+0xc60a2e>
 1208b1b:	0f 1f 44 00 00       	nop    DWORD PTR [rax+rax*1+0x0]
 1208b20:	e8 9b 3a 2f ff       	call   4fc5c0 <_cgo_topofstack@@Base+0x794a0>
 1208b25:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 1208b2c:	00 
 1208b2d:	48 39 cb             	cmp    rbx,rcx
 1208b30:	74 04                	je     1208b36 <crosscall2@@Base+0xc60a16>
 1208b32:	31 c0                	xor    eax,eax
 1208b34:	eb 18                	jmp    1208b4e <crosscall2@@Base+0xc60a2e>
 1208b36:	48 89 c3             	mov    rbx,rax
 1208b39:	48 8b 84 24 e8 01 00 	mov    rax,QWORD PTR [rsp+0x1e8]
 1208b40:	00 
 1208b41:	e8 7a 2a 20 ff       	call   40b5c0 <pam_start_confdir@plt+0x59a8>
 1208b46:	48 8b 8c 24 b0 01 00 	mov    rcx,QWORD PTR [rsp+0x1b0]
 1208b4d:	00 
 1208b4e:	84 c0                	test   al,al
 1208b50:	0f 84 24 ff ff ff    	je     1208a7a <crosscall2@@Base+0xc6095a>
 1208b56:	48 8b 94 24 a8 04 00 	mov    rdx,QWORD PTR [rsp+0x4a8]
 1208b5d:	00 
 1208b5e:	48 89 94 24 40 06 00 	mov    QWORD PTR [rsp+0x640],rdx
 1208b65:	00 
 1208b66:	0f 10 84 24 b0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4b0]
 1208b6d:	00 
 1208b6e:	0f 11 84 24 48 06 00 	movups XMMWORD PTR [rsp+0x648],xmm0
 1208b75:	00 
 1208b76:	0f 10 84 24 c0 04 00 	movups xmm0,XMMWORD PTR [rsp+0x4c0]
 1208b7d:	00 
 1208b7e:	0f                   	.byte 0xf
 1208b7f:	11                   	.byte 0x11
