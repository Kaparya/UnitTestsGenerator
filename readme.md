# UnitTestsGenerator

UnitTestsGenerator - программа, автоматически генерирующая unit-тесты для модулей кода на различных языках. Она будет помогать разработчикам улучшать покрытие кода тестами и тем самым ускорять процесс разработки. Надеемся, AutoUnitTestGenerator поможет разработчикам сконцентрироваться на написании кода, а не создании unit-тестов)

---

## Quick start
1. Устанавливаем зависимости

    ```
    pip install -r requirements.txt
    ```
   
2. Запускаем код

    Общий формат запуска: 
    ```
    ваш_компилятор_питона main.py --file_path <path_to_file>
    ```

   - `--file_path` - параметр, если генерация тестов для одного файла
   - `--folder_path` - если директория

    Примеры:

    ```
   python3 main.py --file_path <path_to_file>
   или
   py main.py --folder_path <path_to_folder>
   ```