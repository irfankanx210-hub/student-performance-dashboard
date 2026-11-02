#  libries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
# page setup
st.set_page_config(page_title="Student Performance Dashboard",layout="wide",)
# title
st.markdown("""
<style>
h1{
    text-align:center;
}
</style>
""",unsafe_allow_html=True
)
st.title("Student Performance Dashboard")
# user upload file
uploaded_file=st.file_uploader(
    "Upload CSV or Excel file",
    type=["csv","xlsx","xls"]
 )
# when file is not None 
if uploaded_file is not None:
    file_name = uploaded_file.name
    # when file csv
    if file_name.endswith(".csv"):
        df=pd.read_csv(uploaded_file)
    # when file Excel
    elif file_name.endswith((".xlsx",".xls")):
        df=pd.read_excel(uploaded_file)
    st.success("File uploaded Successfull")
    # numeric_columns
    numeric_columns=df.select_dtypes(include="number").columns.tolist()
    with st.sidebar:
         selected_menu=option_menu(
              menu_title="Menu",
              options=["Overview","Student Performance","Subject Analysis","Top Performers",
                       "Lowest Performers","Pass/Fail Analysis"],
              icons=["house","person","book","trophy","graph-down","check-circle"]
         )
    # overview (1)
    if selected_menu=="Overview":
        st.title("🏡Overview")
        st.subheader("Dataset Preview")
        st.dataframe(df)
        # select multi_subjects column
        st.subheader("📚Select All Subjects")
        selected_subjects=st.multiselect(
                  "",
                  options=numeric_columns)
        # select student_name column
        st.subheader("🧑‍🎓Select Student_Name")
        selected_student_name=st.selectbox(
             "",
             options=df.columns.tolist())
        if selected_subjects:
            # select student name and columns
            result=df[[selected_student_name] + selected_subjects].copy()
            # calculate total marks for each student
            result["total marks"]=df[selected_subjects].sum(axis=1)
            result["average"]=df[selected_subjects].mean(axis=1)
            st.subheader("📅DataFrame with Total Marks and Average")
            st.dataframe(result)
            st.subheader("📊Distribution of Student Marks")
            # marks distribution
            fig=px.histogram(
                 result,
                 x="total marks",
                 nbins=10,
                 
                 title="Distribution of Student Marks"
                 
            )
            fig.update_traces(marker_line_color="white",marker_line_width=1.5)
            st.plotly_chart(fig)
            # marks vs attendace Scatter plot

            st.subheader("📈Marks vs Attendance")
            st.markdown("""<br />""",unsafe_allow_html=True)
            st.markdown("""<br />""",unsafe_allow_html=True)
            st.subheader("✅Select Attendace_Column")
            selected_attedance=st.selectbox(
                 "",
                 options=numeric_columns   )
            fig=px.scatter(df,
                           x=selected_attedance,
                           y=result["total marks"],
                           hover_name=selected_student_name,
                           title="Attendance vs Academic Performace",)
            st.plotly_chart(fig)
     # Student performance (2)
    elif selected_menu=="Student Performance":
        st.title("🧑‍🎓Individual Student Performance")
        #select student_column
        st.subheader("🧑‍🎓Select Student_Column")
        selected_student_col=st.selectbox(
             label="",
             options=df.columns)
        # select subject_columns
        st.subheader("📚Select All Subjects")
        selected_subjects_cols=st.multiselect(
             "",
             options=numeric_columns)
        # select one student
        st.subheader("🧑‍🎓Select Student Name")
        one_student=st.selectbox(
             "",
            df[selected_student_col].unique())
        student=df[df[selected_student_col] == one_student].iloc[0]
        student_marks=pd.DataFrame({
             "Subject":selected_subjects_cols,
              "Marks"  :[student[s]  for s in selected_subjects_cols]})
        fig=px.bar(
             student_marks,
             x="Subject",
             y="Marks",
             title=f"{one_student} Performance",
             color="Subject",
             text="Marks"
                                )
        st.plotly_chart(
             fig)
        # subject analysis(3)
    elif selected_menu=="Subject Analysis":
         st.title("📕Subject-Wise Analysis")
         st.subheader("📚Select All Subjects")
         selected_subjects=st.multiselect(
              "",
              options=numeric_columns
         )
         st.markdown("""<br />""",unsafe_allow_html=True)
         st.subheader("🧑‍🎓Select Student_Column")
         selected_student_col=st.selectbox(
              "",
              options=df.columns.tolist()
         )
         if selected_subjects:
           # select student name and columns
           result=df[[selected_student_col] + selected_subjects].copy()
           # calculate total marks for each student
           result["total marks"]=df[selected_subjects].sum(axis=1)
           average_marks=df[selected_subjects].mean()
           average_marks=average_marks.reset_index()
           # rename columns
           average_marks.columns=["Subjects","Average_Marks"]
           # create bar chart 
           fig=px.bar(average_marks,
                      x="Subjects",
                      y="Average_Marks",
                      title="Subject-Wise Average Marks",
                      text="Average_Marks",
                      color="Subjects")
           st.plotly_chart(fig)

     # top performaers (4)
    elif selected_menu=="Top Performers":
        st.title("🏆Top 10 Hight Scoring Students")
        # select multi_subjects column
        st.subheader("📚Select All Subjects")
        selected_subjects=st.multiselect(
                                 "",
                                 options=numeric_columns)
        # select student_name column
        st.subheader("🧑‍🎓Select Student_Column")
        selected_student_name=st.selectbox(
                              "",
                              options=df.columns.tolist())
        if selected_subjects:
            # make dataframe which containign names and subject marks
            result2=df[[selected_student_name]+selected_subjects].copy()
            # calculate total marks for each student
            result2["total_marks"]=result2[selected_subjects].sum(axis=1)
            st.subheader("Highest 10 Student")
            # highest 10 students
            top_10=result2.nlargest(10,"total_marks")
            st.dataframe(top_10)
            fig=px.bar(
                 top_10.sort_values("total_marks"),
                 x="total_marks",
                 y=selected_student_name,
                 title="Top 10 Highest Socring Students",
                 color="total_marks",
                 text="total_marks",
                 orientation="h")
            st.plotly_chart(fig)
    elif selected_menu=="Lowest Performers":
            st.title("📉Top 10 Lowest Scoring Students") 
    # select multi_subjects column
            st.subheader("📚Select All Subjects")
            selected_subjects=st.multiselect(
                            "",
                            options=numeric_columns)
            # select student_name column
            st.subheader("🧑‍🎓Select Student_Column")
            selected_student_name=st.selectbox(
                         "",
                         options=df.columns.tolist())
            if selected_subjects:
                # make dataframe which containign names and subject marks
                result2=df[[selected_student_name]+selected_subjects].copy()
                # calculate total marks for each student
                result2["total_marks"]=result2[selected_subjects].sum(axis=1)
                #lowest 10 students
                st.subheader(" Lowest 10 Student")
                lowest_10=result2.nsmallest(10,"total_marks")
                st.dataframe(lowest_10)
                fig=px.bar(
                                 lowest_10.sort_values("total_marks"),
                                 x="total_marks",
                                 y=selected_student_name,
                                 title="Top 10 Lowest Socring Students",
                                 color="total_marks",
                                 text="total_marks",
                                 orientation="h",
                                )
                st.plotly_chart(fig)
     # pass fial analysis
    elif selected_menu == "Pass/Fail Analysis":
        st.title("✅Pass / ❌Fail Analysis")
         # select multi_subjects column
        st.subheader("📚Select All Subjects")
        selected_subjects=st.multiselect(
                          "",
                          options=numeric_columns)
                # select student_name column
        st.subheader("🧑‍🎓Select Student_Name")
        selected_student_name=st.selectbox(
                     "",
                     options=df.columns.tolist())
        if selected_subjects:
          # select student name and columns
          result=df[[selected_student_name] + selected_subjects].copy()
          result["average"]=df[selected_subjects].mean(axis=1)
          # pass and fail pie chart
          result["Result_average"]=result["average"].ge(40).map({True:"Pass",
                                                                 False:"Fail"})
          result_count=(result["Result_average"].value_counts().reset_index())
          result_count.columns=["Result_average",selected_student_name]
          fig=px.pie(result_count,
                     names="Result_average",
                     values=selected_student_name,
                     title="Pass vs Fail Analysis",
                     hole=0.4,)
          st.plotly_chart(fig)
          st.subheader("✅Pass / ❌Fail")
          st.dataframe(result_count)



    # subject wise performance(3)
    elif selected_menu=="Subject wise Performance":
         # numeric column
         numeric_columns=df.select_dtypes(include="number").columns.tolist()
         # slected student name 
         selected_student_name=st.selectbox("Select Student_Name ",
                                            options=df.columns.tolist())
         # selcted subjects
         selected_subject=st.selectbox("Select Subject",
                                       options=numeric_columns)
         # suject performance
         # bar_chart
         st.subheader("Student Performance(Bar Chart)")
         st.bar_chart(data=df,
                      x=selected_student_name,
                      y=selected_subject,
                      x_label=selected_student_name,
                      y_label=selected_subject,
                      color="green",
                      sort=True,
                      )
         # line-chart
         st.subheader("Student Performance(Line Chart)")
         st.line_chart(data=df,
                       x=selected_student_name,
                       y=selected_subject,
                       color="orange",
                       )
# when file is None
elif uploaded_file is None:
        st.warning("Please upload a CSV or Excel file to get started.")
        
