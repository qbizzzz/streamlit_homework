import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency, ttest_ind

def fill_missing_with_median(data):
    return data.fillna(data.median())

def plot_pie_chart(data, col_name):
    counts = data[col_name].value_counts()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(counts, labels=counts.index, autopct="%1.1f%%", startangle=140)
    ax.set_title(f"Распределение {col_name}")
    st.pyplot(fig)

def plot_box_plot(data, col_name):
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=col_name, data=data)
    ax.set_title(f"Распределение {col_name}")
    st.pyplot(fig)

def chi_square_test(data, col_name1, col_name2, alpha):
    contingency_table = pd.crosstab(data[col_name1], data[col_name2])
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    st.write("Результаты Chi-Square теста:")
    st.write(f"Значение Chi-Square: {chi2}")
    st.write(f"P-значение: {p}")
    st.write(f"Степени свободы: {dof}")

    if p < alpha:
        st.write("Связь между переменными статистически значима")
    else:
        st.write("Связь между переменными статистически не значима")

def t_test(data, col_name1, col_name2, alpha):
    group1 = data[data[col_name1].notnull()][col_name1]
    group2 = data[data[col_name2].notnull()][col_name2]

    t_statistic, p_value = ttest_ind(group1, group2)

    st.write("Результаты T-Testа:")
    st.write(f"T-статистика: {t_statistic}")
    st.write(f"P-значение: {p_value}")

    if p_value < alpha:
        st.write("Различия между переменными статистически значимы")
    else:
        st.write("Различия между переменными статистически не значимы")

def main():
    st.title("Обработчик CSV-файлов и Статистические тесты")

    uploaded_file = st.file_uploader("Загрузите CSV-файл", type=["csv"], key="file_upload")

    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.success("Файл успешно загружен!")

            df = fill_missing_with_median(df)

            columns = df.columns.tolist()

            st.subheader("Выбор столбцов")

            selected_col1 = st.selectbox("Выберите первый столбец", columns)
            columns_without_selected = [col for col in columns if col != selected_col1]
            selected_col2 = st.selectbox("Выберите второй столбец", columns_without_selected)

            st.write(f"Выбранные столбцы: {selected_col1}, {selected_col2}")

            st.subheader("Графики распределения")

            if df[selected_col1].dtype == "object" and df[selected_col2].dtype != "object":
                plot_pie_chart(df, selected_col1)
                plot_box_plot(df, selected_col2)
            elif df[selected_col1].dtype != "object" and df[selected_col2].dtype == "object":
                plot_box_plot(df, selected_col1)
                plot_pie_chart(df, selected_col2)
            elif df[selected_col1].dtype == "object" and df[selected_col2].dtype == "object":
                plot_pie_chart(df, selected_col1)
                plot_pie_chart(df, selected_col2)
            else:
                plot_box_plot(df, selected_col1)
                plot_box_plot(df, selected_col2)
            alpha = st.slider("Выберите значение альфа:", min_value=0.01, max_value=0.1, step=0.01, value=0.05)
            st.write(f"Выбранное значение альфа: {alpha}")
            methods = ["Выберите метод", "Chi-Square Test", "T-Test"]
            selected_method = st.selectbox("Выберите метод статистической проверки:", methods)
            if selected_method != "Выберите метод":
                st.subheader("Результаты статистической проверки")
                if selected_method == "Chi-Square Test":
                    chi_square_test(df, selected_col1, selected_col2, alpha)
                elif selected_method == "T-Test":
                    t_test(df, selected_col1, selected_col2, alpha)
        except pd.errors.ParserError:
            st.error("Ошибка: Неверный формат CSV-файла. Загрузите действительный CSV-файл.")

if __name__ == "__main__":
    main()
