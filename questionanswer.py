
import os
import sys
import logging

import xml.dom.minidom
from xml.dom.minidom import parse, parseString

from ternip.formats.timex3 import Timex3XmlDocument
from ternip.timex import Timex


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename='questionanswer.log',
                    filemode='w')


class questionanswer():
	"""
	questionanswer 
	"""
	

	def __init__(self):
		self.kblist=[]
		self.tags=[]
		self.lineno_ORG={}
		self.lineno_per={}
		self.lineno_loc={}
		self.parsefile(sys.argv[1])
		self.parsener()
		self.parsetimex()
		
	def askquestion(self,inquestion):
		"""
		parse the given question.

		"""
		questionwords=inquestion.split()

		if len(questionwords)<2:
			print "Not very clear can you elaborate ..?"

		if 'who' in questionwords:
			logging.info('who question :'+inquestion)
			qtype=1
			remquestion=' '.join(questionwords[questionwords.index('who')+1:])
			print "ANS:-------------------------------------"
			print self.getanswer(qtype,remquestion)
		elif 'what' in questionwords:
			qtype=2
		elif 'when' in questionwords:
			qtype=3
		elif 'where' in questionwords:
			qtype=4
			remquestion=' '.join(questionwords[questionwords.index('who')+1:])
			print self.getanswer(qtype,remquestion)

		return qtype

	def giveanswer():

		if qtype==1:
			atype=1
		return


	def parsefile(self,kbfile):
		"""
		This fuction takes the kbfile as input parseit line by line and do Named entity as well timex3 annotation 
		also create a dictionary of entity and timex3 on line as key
		"""
		f= open(kbfile,'r')
		for line in f:
			self.kblist.append(line)
		print kbfile
		timex3path='/home/nitin/casestudy/ternip-master/'
		print 'timex3 tagging'
		#os.chdir(timex3path)
		#retval = os.getcwd()
		#print retval
		program_str='./annotate_timex'
		option='--doctype timex3'
		infile=kbfile
		redirect='>'
		outfile=kbfile+'.timex3'

		cmd_str = ''.join([program_str, ' ', option, ' ', infile, ' ',redirect,' ',outfile])
		os.system(cmd_str)
		#os.system('ternip-master/annotate_timex --doctype timex3 $kbfile >$kbfile.ner')
		#os.system('./annotate_timex --doctype timex3 $1 > ${1}.ner')    
		print 'doing ner'
		program_str='sh stanford-ner-2013-04-04/ner.sh'
		option='--doctype timex3'
		infile=kbfile
		redirect='>'
		outfile=kbfile+'.ner'
		cmd_str = ''.join([program_str, ' ', infile, ' ',redirect,' ',outfile])
		os.system(cmd_str)

	def parsetimex(self,timex3file='test.xml.timex3'):
		timex3_file=open(timex3file,'r')
		#s = Timex3XmlDocument(timex3_file.read())
		
		d=parse(timex3_file)
		#t = Timex(type='date')
		print d.documentElement.tagName == "DATE"
		
		return

	def parsener(self,ner_file='test.xml.ner'):
		nerfile=open(ner_file,'r')
		lno=1
		line_ner={}
		for line in nerfile:
			logging.info(line.split())
			tokens=line.split()

			tags=[(tok.split('/')[0],tok.split('/')[1],lno) for tok in tokens]
			
			for i in range(len(tags)):
				if tags[i][1]=='PERSON':
					if lno in self.lineno_per.keys(): 
						self.lineno_per[lno].append(tags[i][0])

					else:
						#print tags[i][0]
						self.lineno_per[lno]=[tags[i][0]]

			for i in range(len(tags)):
				if tags[i][1]=='ORGANIZATION':
					if lno in self.lineno_ORG.keys():

						self.lineno_ORG[lno].append(tags[i][0])
					else:
						self.lineno_ORG[lno]=[tags[i][0]]

			for i in range(len(tags)):
				if tags[i][1]=='LOCATION':
					if lno in self.lineno_loc.keys():
						self.lineno_loc[lno].append(tags[i][0])
					else:
						self.lineno_loc[lno]=[tags[i][0]]
			lno+=1
			logging.info(self.lineno_per)
			logging.info(self.lineno_loc)
			logging.info(self.lineno_ORG)
			logging.info(tags)
		self.tags=tags

			#print tags
			#line_ner[]
		return

	def getanswer(self,qtype,remquestion):
		logging.info(remquestion)
		logging.info(qtype)
		if qtype==1:
			lineno=1
			#print kblist
			for line in self.kblist:
				#print line
				if remquestion in line :
					#print line
					ans=''.join(self.lineno_per[lineno][0])

				lineno+=1
		if qtype==4:
			lineno=1
			#print kblist
			for line in self.kblist:
				#print line
				if remquestion in line :
					#print line
					ans=''.join(self.lineno_ORG[lineno][0])

				lineno+=1

		return ans+' '+remquestion
if __name__ == "__main__":
	q=questionanswer()
	#q.parsefile(sys.argv[1])
	#q.parsener()
	#q.parsetimex()
	q.askquestion(sys.argv[2])



