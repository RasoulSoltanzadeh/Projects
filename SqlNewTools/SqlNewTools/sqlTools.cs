using System;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Data;
using System.Data.SqlClient;

namespace SqlNewTools
{
    class sqlTools
    {
        //Properties----------------------------------------------------------------------------------------------------------------------
        public static string connectionString { get; set; }
        private static bool RecordEvent { get; set; } = true;
        private static bool DeleteEvent { get; set; } = true;
        private static bool InsertEvent { get; set; } = true;
        //Structs------------------------------------------------------------------------------------------------------------------------
        public struct CollectionName
        {
            public const string Tables = "Tables";
            public const string Columns = "Columns";
            public const string Indexes = "Indexes";
            public const string Views = "Views";
            public const string Procedures = "Procedures";
        }
        //Event--------------------------------------------------------------------------------------------------------------------------
        public delegate void Event(object sender, object values, DataTable table, Exception EX);
        public delegate void Eventing(object sender, DataTable table, Exception EX);
        public static event Event Inserting;
        public static event Event Insered;
        public static event Event InsertException;
        public static event Event Deleting;
        public static event Event Deleted;
        public static event Event DeleteException;
        public static event Eventing Selecting;
        public static event Event Selected;
        public static event Eventing SelectException;
        public static event Event Updating;
        public static event Event Updated;
        public static event Event UpdateException;
        public static event Event AntiRepeating;
        public static event Event AntiRepeated;
        //EventMethods------------------------------------------------------------------------------------------------------------------
        public static void DoInserting(object sender, object values, DataTable table, Exception EX) { if (InsertEvent) Inserting(sender, values, table, EX); }
        public static void DoInsered(object sender, object values, DataTable table, Exception EX) { if (InsertEvent) Insered(sender, values, table, EX); }
        public static void DoInsertException(object sender, object values, DataTable table, Exception EX) { if (InsertEvent) InsertException(sender, values, table, EX); }
        public static void DoDeleting(object sender, object values, DataTable table, Exception EX) { if (DeleteEvent) Deleting(sender, values, table, EX); }
        public static void DoDeleted(object sender, object values, DataTable table, Exception EX) { if(DeleteEvent) Deleted(sender, values, table, EX); }
        public static void DoDeleteException(object sender, object values, DataTable table, Exception EX) { if (DeleteEvent) DeleteException(sender, values, table, EX); }
        public static void DoSelecting(object sender, DataTable table, Exception EX) { if (RecordEvent) Selecting(sender, table, EX); }
        public static void DoSelected(object sender, object values, DataTable table, Exception EX) { if (RecordEvent) Selected(sender, values, table, EX); }
        public static void DoSelectException(object sender, DataTable table, Exception EX) { if (RecordEvent) SelectException(sender, table, EX); }
        public static void DoUpdating(object sender, object values, DataTable table, Exception EX) { Updating(sender, values, table, EX); }
        public static void DoUpdated(object sender, object values, DataTable table, Exception EX) { Updated(sender, values, table, EX); }
        public static void DoUpdateException(object sender, object values, DataTable table, Exception EX) { UpdateException(sender, values, table, EX); }
        public static void DoAntiRepeating(object sender, object values, DataTable table, Exception EX) { AntiRepeating(sender, values, table, EX); }
        public static void DoAntiRepeated(object sender, object values, DataTable table, Exception EX) { AntiRepeated(sender, values, table, EX); }
        //Methods------------------------------------------------------------------------------------------------------------------------
        public static Exception Insert(string TableName, params object[] objs)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            Exception EX = new Exception();
            try
            {
                connection.Open();
                DoInserting(new object(), objs, GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Insert Into {TableName} Values ({GetSqlSrting(objs)})";
                command.ExecuteNonQuery();
                DoInsered(new object(), objs, GetDataTable(TableName, out EX), EX);
            }
            catch (Exception ex)
            {
                DoInsertException(new object(), objs, GetDataTable(TableName, out EX), ex);
                return ex;
            }
            finally
            {
                connection.Close();
            }
            return new Exception("No Exception");
        }
        public static Exception Delete(string TableName, int RowIndex)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            Exception EX = new Exception();
            try
            {
                connection.Open();
                DoDeleting(new object(), GetDataTable(TableName, out EX).Rows[RowIndex].ItemArray, GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Delete from {TableName} where {GetPrimaryKeyNames(TableName, out EX)[0]} = {GetSqlSrting(((object[])GetTable(TableName, out EX)[RowIndex])[GetColumnIndex(TableName, GetPrimaryKeyNames(TableName, out EX)[0], out EX)])}";
                command.ExecuteNonQuery();
                DoDeleted(new object(), GetDataTable(TableName, out EX).Rows[RowIndex].ItemArray, GetDataTable(TableName, out EX), EX);
                return EX;
            }
            catch (Exception ex)
            {
                DoDeleteException(new object(), GetDataTable(TableName, out EX).Rows[RowIndex].ItemArray, GetDataTable(TableName, out EX), ex);
                return ex;
            }
            finally
            {
                connection.Close();
            }
        }
        public static Exception Delete(string TableName, object ColumnValue, string ColumnName)
        {
            RecordEvent = false;
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            Exception EX = new Exception("No Exception");
            try
            {
                connection.Open();
                DoDeleting(new object(), GetRecord(TableName, ColumnValue, ColumnName, out EX), GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Delete from {TableName} where {ColumnName} = {GetSqlSrting(ColumnValue)}";
                command.ExecuteNonQuery();
                DoDeleted(new object(), GetRecord(TableName, ColumnValue, ColumnName, out EX), GetDataTable(TableName, out EX), EX);
                return EX;
            }
            catch (Exception ex)
            {
                DoDeleteException(new object(), GetRecord(TableName, ColumnValue, ColumnName, out EX), GetDataTable(TableName, out EX), ex);
                return ex;
            }
            finally
            {
                connection.Close();
                RecordEvent = true;
            }
        }
        public static Exception Delete(string TableName, object[] ColumnValues, string[] ColumnNames)
        {
            RecordEvent = false;
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            Exception EX = new Exception("No Exception");
            try
            {
                string[] Values = GetSqlSrting(ColumnValues).Split(new char[] { ',' });
                string[] SqlString = new string[ColumnNames.Length];
                string Out = "";
                for (int i = 0; i < ColumnNames.Length; i++) SqlString[i] = $"{ColumnNames[i]} = {Values[i]}";
                Out = string.Join(" and ", SqlString);
                connection.Open();
                DoDeleting(new object(), GetRecord(TableName, ColumnValues, ColumnNames, out EX), GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Delete from {TableName} where ({Out})";
                command.ExecuteNonQuery();
                DoDeleted(new object(), GetRecord(TableName, ColumnValues, ColumnNames, out EX), GetDataTable(TableName, out EX), EX);
                return EX;
            }
            catch (Exception ex)
            {
                DoDeleteException(new object(), GetRecord(TableName, ColumnValues, ColumnNames, out EX), GetDataTable(TableName, out EX), ex);
                return ex;
            }
            finally
            {
                connection.Close();
                RecordEvent = true;
            }
        }
        public static ArrayList GetRecord(string TableName, int RowIndex, out Exception EX)
        {
            ArrayList Row = new ArrayList();
            EX = new Exception("No Exception");
            try
            {
                DoSelecting(new object(), GetDataTable(TableName, out EX), EX);
                Row.Add((object[])GetTable(TableName, out EX)[RowIndex]);
                DoSelected(new object(), (object[])GetTable(TableName, out EX)[RowIndex], GetDataTable(TableName, out EX), EX);
                return Row;
            }
            catch (Exception ex)
            {
                EX = ex;
                DoSelectException(new object(), GetDataTable(TableName, out EX), ex);
                return new ArrayList();
            }
        }
        public static ArrayList GetRecord(string TableName, object ColumnValue, string ColumnName, out Exception EX)
        {
            int i = 0;
            ArrayList Rows = new ArrayList();
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            SqlDataReader reader;
            EX = new Exception("No Exception");
            try
            {
                connection.Open();
                DoSelecting(new object(), GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Select * from {TableName} where {ColumnName} = {GetSqlSrting(ColumnValue)}";
                reader = command.ExecuteReader();
                while (reader.Read())
                {
                    Rows.Add(new object[GetColumnsCount(TableName, out EX)]);
                    reader.GetValues((object[])Rows[i++]);
                }
                DoSelected(new object(), Rows, GetDataTable(TableName, out EX), EX);
                return Rows;
            }
            catch (Exception ex)
            {
                EX = ex;
                DoSelectException(new object(), GetDataTable(TableName, out EX), ex);
                return new ArrayList();
            }
            finally
            {
                connection.Close();
            }
        }
        public static ArrayList GetRecord(string TableName, object[] ColumnValues, string[] ColumnNames, out Exception EX)
        {
            int j = 0;
            ArrayList Rows = new ArrayList();
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            SqlDataReader reader;
            EX = new Exception("No Exception");
            string[] sql = GetSqlSrting(ColumnValues).Split(',');
            string[] str = ColumnNames;
            string Out = "";
            for (int i = 0; i < ColumnNames.Length; i++) str[i] = $"{str[i]} = {sql[i]}";
            Out = string.Join(" And ", str);
            try
            {
                connection.Open();
                DoSelecting(new object(), GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Select * from {TableName} where ({Out})";
                reader = command.ExecuteReader();
                while (reader.Read())
                {
                    Rows.Add(new object[GetColumnsCount(TableName, out EX)]);
                    reader.GetValues((object[])Rows[j++]);
                }
                DoSelected(new object(), Rows, GetDataTable(TableName, out EX), EX);
                return Rows;
            }
            catch (Exception ex)
            {
                EX = ex;
                DoSelectException(new object(), GetDataTable(TableName, out EX), ex);
                return new ArrayList();
            }
            finally
            {
                connection.Close();
            }
        }
        public static Exception Update(string TableName, params object[] objs)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            Exception EX = new Exception("No Exception");
            try
            {
                connection.Open();
                DoUpdating(new object(), objs, GetDataTable(TableName, out EX), EX);
                command.CommandText = $"Update {TableName} set {GetSqlSrting(objs)}";
                command.ExecuteNonQuery();
                DoUpdated(new object(), objs, GetDataTable(TableName, out EX), EX);
                return EX;
            }
            catch (Exception ex)
            {
                DoUpdateException(new object(), objs, GetDataTable(TableName, out EX), ex);
                return ex;
            }
            finally
            {
                connection.Close();
            }
        }
        public static Exception AntiRepetition(string TableName, int RowIndex, string ColumnKayName)
        {
            RecordEvent = false;
            DeleteEvent = false;
            InsertEvent = false;
            Exception EX = new Exception();
            ArrayList array = new ArrayList();
            object[] objs = new object[0];
            DoAntiRepeating(new object(), (object[])GetRecord(TableName, RowIndex, out EX)[0], GetDataTable(TableName, out EX), EX);
            objs = (object[])GetRecord(TableName, RowIndex, out EX)[0];
            Delete(TableName, objs[Array.IndexOf<string>(GetColumnNames(TableName, out EX), ColumnKayName)], ColumnKayName);
            EX = Insert(TableName, objs);
            DoAntiRepeated(new object(), (object[])GetRecord(TableName, RowIndex, out EX)[0], GetDataTable(TableName, out EX), EX);
            RecordEvent = true;
            DeleteEvent = true;
            InsertEvent = true;
            return EX;
        }
        public static Exception AntiRepetition(string TableName, object[] ColumnKeyValue, string[] ColumnKayName)
        {
            RecordEvent = false;
            DeleteEvent = false;
            InsertEvent = false;
            Exception EX = new Exception();
            ArrayList array = new ArrayList();
            object[] objs = new object[0];
            DoAntiRepeating(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[0], GetDataTable(TableName, out EX), EX);
            objs = (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[0];
            Delete(TableName, ColumnKeyValue, ColumnKayName);
            EX = Insert(TableName, objs);
            DoAntiRepeated(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[0], GetDataTable(TableName, out EX), EX);
            RecordEvent = true;
            DeleteEvent = true;
            InsertEvent = true;
            return EX;
        }
        public static Exception LastAntiRepetition(string TableName, object ColumnKeyValue, string ColumnKayName)
        {
            RecordEvent = false;
            DeleteEvent = false;
            InsertEvent = false;
            Exception EX = new Exception();
            ArrayList array = new ArrayList();
            object[] objs = new object[0];
            DoAntiRepeating(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1], GetDataTable(TableName, out EX), EX);
            objs = (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1];
            Delete(TableName, ColumnKeyValue, ColumnKayName);
            EX = Insert(TableName, objs);
            DoAntiRepeated(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1], GetDataTable(TableName, out EX), EX);
            RecordEvent = true;
            DeleteEvent = true;
            InsertEvent = true;
            return EX;
        }
        public static Exception LastAntiRepetition(string TableName, object[] ColumnKeyValue, string[] ColumnKayName)
        {
            RecordEvent = false;
            DeleteEvent = false;
            InsertEvent = false;
            Exception EX = new Exception();
            ArrayList array = new ArrayList();
            object[] objs = new object[0];
            DoAntiRepeating(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1], GetDataTable(TableName, out EX), EX);
            objs = (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1];
            Delete(TableName, ColumnKeyValue, ColumnKayName);
            EX = Insert(TableName, objs);
            DoAntiRepeated(new object(), (object[])GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX)[GetRecord(TableName, ColumnKeyValue, ColumnKayName, out EX).Count - 1], GetDataTable(TableName, out EX), EX);
            RecordEvent = true;
            DeleteEvent = true;
            InsertEvent = true;
            return EX;
        }
        public static ArrayList GetTable(string TableName, out Exception EX)
        {
            ArrayList Rows = new ArrayList();
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            SqlDataReader reader;
            EX = new Exception("No Exception");
            int i = 0;
            try
            {
                connection.Open();
                command.CommandText = $"Select * from {TableName}";
                reader = command.ExecuteReader();
                while (reader.Read())
                {
                    Rows.Add(new object[GetColumnsCount(TableName, out EX)]);
                    reader.GetValues((object[])Rows[i++]);
                }
                return Rows;
            }
            catch (Exception ex)
            {
                EX = ex;
                return new ArrayList();
            }
            finally
            {
                connection.Close();
            }
        }
        public static string GetSqlSrting(params object[] objs)
        {
            string str = "";
            for (int i = 0; i < objs.Length; i++)
            {
                objs[i] = "N'" + objs[i].ToString() + "'";
                str += "," + objs[i].ToString();
            }
            str = str.Remove(0, 1);
            return str;
        }
        public static int GetColumnIndex(string TableName, string ColumnName, out Exception EX)
        {
            int Index = -1;
            string[] str = new string[0];
            try
            {
                str = GetColumnNames(TableName, out EX);
                for (int i = 0; i < str.Length; i++) Index = str[i] == ColumnName ? i : Index;
                return Index;
            }
            catch (Exception ex)
            {
                EX = ex;
                return Index;
            }
        }
        public static string[] GetColumnNames(string TableName, out Exception EX)
        {
            string[] Names;
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            SqlDataReader reader;
            DataTable table;
            try
            {
                connection.Open();
                command.CommandText = $"Select * from {TableName}";
                reader = command.ExecuteReader();
                table = reader.GetSchemaTable();
                Names = new string[GetColumnsCount(TableName, out EX)];
                for (int i = 0; i < Names.Length; i++) Names[i] = table.Rows[i][0].ToString();
                return Names;
            }
            catch (Exception ex)
            {
                EX = ex;
                return new string[0];
            }
            finally
            {
                connection.Close();
            }
        }
        public static int GetColumnsCount(string TableName, out Exception EX)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlCommand command = new SqlCommand("", connection);
            SqlDataReader reader;
            DataTable table;
            try
            {
                connection.Open();
                command.CommandText = $"Select * from {TableName}";
                reader = command.ExecuteReader();
                table = reader.GetSchemaTable();
                EX = new Exception("No Exception");
                return table.Rows.Count;
            }
            catch (Exception ex)
            {
                EX = ex;
                return -1;
            }
            finally
            {
                connection.Close();
            }
        }
        public static string[] GetPrimaryKeyNames(string TableName, out Exception EX)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlDataAdapter adapter = new SqlDataAdapter($@"Select COLUMN_NAME from INFORMATION_SCHEMA.KEY_COLUMN_USAGE where TABLE_NAME = '{TableName}'", connection);
            DataTable table = new DataTable();
            string[] str = new string[0];
            EX = new Exception("No Exception");
            try
            {
                connection.Open();
                adapter.Fill(table);
                str = new string[table.Rows.Count];
                for (int i = 0; i < str.Length; i++) str[i] = table.Rows[i][0].ToString();
                return str;
            }
            catch (Exception ex)
            {
                EX = ex;
                return new string[0];
            }
            finally
            {
                connection.Close();
            }
        }
        public static DataTable GetDataTable(string TableName, out Exception EX)
        {
            SqlConnection connection = new SqlConnection(connectionString);
            SqlDataAdapter adapter = new SqlDataAdapter($"Select * from {TableName}", connection);
            DataTable table = new DataTable(TableName);
            EX = new Exception("No Exception");
            try
            {
                connection.Open();
                adapter.Fill(table);
                return table;
            }
            catch (Exception ex)
            {
                EX = ex;
                return new DataTable();
            }
            finally
            {
                connection.Close();
            }
        }
        public void AddToForwarder(string ForwarderName, object FirstValue, object[] LastValues, out Exception EX)
        {
            EX = new Exception("No Exeption");
            int count = GetRowsCount(ForwarderName, out EX);
            try
            {
                foreach (var item in LastValues) Insert(ForwarderName, count += 1, FirstValue, item);
            }
            catch (Exception ex)
            {
                EX = ex;
            }
        }
        public static int GetRowIndex(string TableName, object[] Row, out Exception EX)
        {
            EX = new Exception("No Exception");
            DataRowCollection dataRow = GetDataTable(TableName, out EX).Rows;
            ArrayList array = GetTable(TableName, out EX);
            string str1 = GetSqlSrting(Row);
            string[] str2 = new string[array.Count];
            for (int i = 0; i < array.Count; i++) str2[i] = GetSqlSrting((object[])array[i]);
            return Array.IndexOf<string>(str2, str1);
        }
        public static int GetRowsCount(string TableName, out Exception EX) { return GetDataTable(TableName, out EX).Rows.Count; }
    }
}
