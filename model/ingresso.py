from database import Database

class Ingresso():
	def __init__(self):
		self.table = "Ingresso"
		self.db = Database().conn()
		self.cursor = self.db.cursor()

	def findAll(self,usuario_id):		
		try:
			sql = "SELECT Id, Tipo, Quantidade, Preco, Evento_Id FROM %s WHERE Usuario_Id = ?" % self.table
			self.cursor.execute(sql,[usuario_id])
			return self.cursor.fetchall()
		except Exception:
			self.db.close()
			
	def find(self,Usuario_Id,Id):
		try:
			sql = "SELECT * FROM %s WHERE Usuario_Id = ? AND Id = ?" % self.table
			self.cursor.execute(sql,[Usuario_Id,Id])
			return self.cursor.fetchone()
		except Exception:
			self.db.close()

	def update(self,Tipo,Quantidade,Preco,Evento_Id,Usuario_Id,Id):
		try:
			print quantidade
			sql = "UPDATE %s SET Tipo = ? , Quantidade = ?, Preco = ?, Evento_Id = ? WHERE Usuario_Id = ? AND Id = ?" % self.table
			self.cursor.execute(sql,[Tipo,Quantidade,Preco,Evento_Id,Usuario_Id,Id])
			self.db.commit()
			self.db.close()
			return True
		except Exception:
			return False

	def add(self,Tipo,Quantidade,Preco,Usuario_Id,Evento_Id):
		try:
			sql = "INSERT INTO %s (Tipo,Quantidade,Preco,Usuario_Id,Evento_Id) VALUES (?,?,?,?,?)" % self.table
			self.cursor.execute(sql,[Tipo,Quantidade,Preco,Usuario_Id,Evento_Id])
			self.db.commit()
			self.db.close()
			return True
		except Exception:
			return False

	def delete(self,Usuario_Id,Id):
		try:
			sql = "DELETE FROM %s WHERE Usuario_Id = ? AND Id = ?" % self.table
			self.cursor.execute(sql,[Usuario_Id,Id])
			self.db.commit()
			self.db.close()
			return True
		except Exception:
			return False
	def delete_all(self,usuario_id):
			try:
				sql = "DELETE FROM %s WHERE Usuario_Id = ?" % self.table
				self.cursor.execute(sql,[usuario_id])
				self.db.commit()
				self.db.close()
				return True
			except Exception:
				return False
