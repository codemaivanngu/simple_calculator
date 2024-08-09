from streamlit import session_state
import streamlit as st
CC1,CC2 = st.columns([1.3,1])
with CC1:
    with st.container(border=True):
        DELTA = 1e-6
        st.header('Simple Calculator 🧮')
        if 'L' not in session_state:
            session_state.L=[]
        if 's' not in session_state:
            session_state.s=''

        operator_map ={
            '/': '÷',
            '*': '×',
            '-': '−',
            '+': '➕'
        }

        stack=[]
        def cal():
            print(session_state.L)
            

            def convert_notation(mention_operators):
                for i in range(len(session_state.L)-1,-1,-1):
                    if session_state.L[i] in mention_operators:
                        print("================",i,len(session_state.L),session_state.L[i])
                        session_state.L[i],session_state.L[i+1]=session_state.L[i+1],session_state.L[i]
                        i+=1
                print("after convert notation",session_state.L)
            def cal(mention_operators):
                global stack
                for c in session_state.L:
                    if c in mention_operators:
                        t1=float(stack[-2])
                        t2=float(stack[-1])
                        stack.pop()
                        stack.pop()
                        if c=='+':t1+=t2
                        if c=='-':t1-=t2
                        if c=="*":t1*=t2
                        if c=='/':
                            if t2==0:
                                session_state.L=["nan"]
                                stack=['nan']
                                return
                            t1/=t2
                        if(abs(t1-round(t1))<DELTA):t1 = round(t1)
                        t1=str(t1)  
                        stack.append(t1)
                    else: stack.append(c)
                    print(stack)
                session_state.L=stack
                stack = []
            convert_notation("*/")
            cal("*/")
            convert_notation("+-")
            cal("+-")
            session_state.s=session_state.L[0]
            session_state.L=[]


        def F(ss):
            if ss == "=":
                if session_state.s=="":
                    print("weird")
                    return
                session_state.L.append(session_state.s)
                session_state.s=""
                cal()
                return 
            if ss in "+-*/":
                if session_state.s=="":return
                session_state.L.append(session_state.s)
                session_state.L.append(ss)
                session_state.s=""
                return 

            if ss=='.':
                if "." in session_state.s: return
                if len(session_state.s) and session_state.s[-1]=='.':return
            if session_state.s=="0" and ss!='.':
                session_state.s=ss
                return
                # if session_state.s=="0":return
            if session_state.s == "nan":
                session_state.s=""
                # return
            session_state.s=session_state.s+ss

        c1,c2 = st.columns([3,1])
        with c1:
            with st.container(border=True,height=80):
                if(session_state.s!=""):
                    st.markdown(session_state.s)
                else: st.markdown("_")
                st.caption(" ".join(session_state.L))
        with c2:
            def FAC(back=0):
                if back and session_state.s!="": session_state.s=session_state.s[:-1]
                elif session_state.s!="":session_state.s=""
                else: session_state.L=[]
                
            st.button("AC",type="secondary",use_container_width=True,on_click=lambda:FAC())
            st.button("←",type="secondary",use_container_width=True,on_click=lambda:FAC(1))
            # col2.button('←', on_click=on_click, args=('←',))

        with st.container():
            c1,c2,c3,c4 = st.columns(4)
            with c1:
                for i in [7,4,1,0]:
                    st.button(str(i),type="secondary",use_container_width=True,on_click=lambda i=i:F(str(i)))

            with c2:
                for i in [8,5,2,'.']:
                    st.button(str(i),type="secondary",use_container_width=True,on_click=lambda i=i:F(str(i)))
                
            with c3:
                for i in [9,6,3,"="]:
                    st.button(str(i),type="secondary",use_container_width=True,on_click=lambda i=i:F(str(i)))
            
            with c4:
                for i in ["/","*","+","-"]:
                    st.button(operator_map[i],type="primary",use_container_width=True,on_click=lambda i=i:F(str(i)[0]))
