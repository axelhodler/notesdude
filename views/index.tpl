% rebase layout
<p>Notes</p>
<form action="/new">
      <input type="submit" value="New Note">
</form>
<table border="1">
%for row in rows:
  <tr>
    <td>{{row.get('id')}}</td>
    <td>{{row.get('title')}}</td>
    <td>{{row.get('content')}}</td>
    <td><form action="/delete/{{row.get('id')}}">
              <input type="submit" value="Delete Note">
        </form>
    </td>
  </tr>
%end
</table>